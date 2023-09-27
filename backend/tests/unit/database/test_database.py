# import pytest
# from src.database.Database import Database
# from src.database.Room import Room, RoomStatus
# from src.database.Question import Question
# from src.database.User import User
# from src.database.Option import Option
#
#
# def test_query_room_data(mock_redis, sample_room):
#     # Test querying a room + storing room data
#     pipeline = mock_redis.r.pipeline()
#     mock_redis.store_room_data(sample_room.room_id, sample_room, pipeline)
#
#     # Query the room data
#     queried_room = mock_redis.query_room_data(sample_room.room_id)
#
#     # Check if the queried room data matches the original room data
#     assert queried_room == sample_room
#
#
# def test_query_room_data_dict(mock_redis, sample_room):
#     # Test querying a room in dict form
#     mock_redis.store_room_data(sample_room.room_id, sample_room)
#
#     # Query the room data
#     queried_room = mock_redis.query_room_data(sample_room.room_id, True)
#
#     # Check if the queried room data matches the original room data
#     assert queried_room == sample_room.to_dict()
#
#
# def test_remove_room_data(mock_redis, sample_room):
#     # Store a room in the database
#     mock_redis.store_room_data(sample_room.room_id, sample_room)
#
#     # Test removing room data
#     result = mock_redis.remove_room_data(sample_room.room_id)
#
#     # Check that the operation was successful
#     assert result == 1
#
#
# def test_add_user(mock_redis, sample_room):
#     # Store a room in the database
#     mock_redis.store_room_data(sample_room.room_id, sample_room)
#
#     # Test adding a user
#     num_users = mock_redis.add_user(room_id=sample_room.room_id, user_id="u3", username="Charles")
#
#     # Query the room data
#     queried_room = mock_redis.query_room_data(sample_room.room_id)
#
#     assert len(queried_room.users) == num_users
#
#
# def test_get_users(mock_redis, sample_room):
#     # Store a room in the database
#     mock_redis.store_room_data(sample_room.room_id, sample_room)
#
#     # Test getting users
#     users = mock_redis.get_users(sample_room.room_id)
#
#     # Check that the user is in the list of users
#     assert len(users) == len(sample_room.users)
#     assert users[0]["user_id"] == "u1"
#
#
# def test_remove_users(mock_redis, sample_room):
#     # Store a room in the database
#     mock_redis.store_room_data(sample_room.room_id, sample_room)
#
#     result = mock_redis.remove_users(sample_room.room_id, "u2")
#
#     # Check that the operation was successful
#     assert result is True
#
#
# def test_get_questions(mock_redis, sample_room):
#     mock_redis.store_room_data(sample_room.room_id, sample_room.room_code, sample_room)
#     questions = mock_redis.get_questions(sample_room.room_id)
#     assert len(questions) == 1
#     assert questions[0]["question_id"] == "q1"
#
#
# def test_insert_question(mock_redis, sample_room):
#     mock_redis.store_room_data(sample_room.room_id, sample_room.room_code, sample_room)
#     question = Question(
#         question_id="q3",
#         question_text="What's your favorite animal?",
#         options=[Option("o1", "dinosaur", 3)],
#     )
#
#     # Test inserting a question
#     result = mock_redis.insert_question(sample_room.room_id, question)
#
#     # Check that the operation was successful
#     assert result is True
#
#
# # def test_get_options(mock_redis):
# #
# #
# #     mock_redis.store_room_data(sample_room.room_id, sample_room.room_code, sample_room)
# #     options = mock_redis.get_options(sample_room.room_id, sample_room.questions[0]["q1"])
# #
# #     # Check that the option is in the list of options
# #     assert len(options) == 1
# #     assert options[0]["option_id"] == "o1"
#
#
# # def test_update_options(mock_redis): #     room_id = "sample_room" #     question_id = "q1" #     option =
# Option(option_id="o1", option_text="Blue", current_votes=5) # #     # Test updating options #     result =
# mock_redis.update_options(room_id, question_id, option) # #     # Check that the operation was successful #
# assert result is True # # # def test_get_vote(mock_redis): #     room_id = "sample_room" #     question_id = "q1" #
# option_id = "o1" #     option = Option(option_id=option_id, option_text="Green", current_votes=3) #
# mock_redis.store_single_field(room_id, "questions", [{"question_id": question_id, "options": [option.to_dict()]}],
#                                True) # #     # Test getting the vote count #     vote_count = mock_redis.get_vote(
#                                room_id, question_id, option_id) # #     # Check that the vote count matches the
#                                stored value #     assert vote_count == 3 # # # def test_increment_vote(mock_redis):
#     room_id = "sample_room" #     question_id = "q1" #     option_id = "o1" # #     # Test incrementing the vote
#     count #     result = mock_redis.increment_vote(room_id, question_id, option_id) # #     # Check that the
#     operation was successful #     assert result is True # # # def test_decrement_vote(mock_redis): #     room_id =
#     "sample_room" #     question_id = "q1" #     option_id = "o1" # #     # Test decrementing the vote count #
#     result = mock_redis.decrement_vote(room_id, question_id, option_id) # #     # Check that the operation was
#     successful #     assert result is True # # # def test_update_room_activity_time(mock_redis): #     room_id =
#     "sample_room" #     new_activity_time = datetime.now() # #     # Test updating the room's activity time #
#     result = mock_redis.update_room_activity_time(room_id, new_activity_time) # #     # Check that the operation
#     was successful #     assert result is True # # # def test_get_room_location(mock_redis): #     room_id =
#     "sample_room" #     location = "Living Room" #     mock_redis.store_single_field(room_id, "room_location",
#     location) # #     # Test getting the room's location #     retrieved_location = mock_redis.get_room_location(
#     room_id) # #     # Check that the retrieved location matches the stored location #     assert
#     retrieved_location == location # # # def test_update_room_location(mock_redis): #     room_id = "sample_room" #
#     new_location = "Bedroom" # #     # Test updating the room's location #     result =
#     mock_redis.update_room_location(room_id, new_location) # #     # Check that the operation was successful #
#     assert result is True # # # def test_get_room_activity(mock_redis): #     room_id = "sample_room" #
#     activity = "Watching TV" #     mock_redis.store_single_field(room_id, "room_activity", activity) # #     # Test
#     getting the room's activity #     retrieved_activity = mock_redis.get_room_activity(room_id) # #     # Check
#     that the retrieved activity matches the stored activity #     assert retrieved_activity == activity # # #
#     def test_update_room_activity(mock_redis): #     room_id = "sample_room" #     new_activity = "Reading" # #
# Test updating the room's activity #     result = mock_redis.update_room_activity(room_id, new_activity) # #     #
# Check that the operation was successful #     assert result is True
#
#
# def test_query_all_hash_keys(mock_redis):
#     # This test is for the query_all_hash_keys method, which prints information but doesn't return values.
#     pass
#
#     # Example usage:
#     # Create a room, add users, questions, and options
#     # room = Room(
#     #     room_id="r1",
#     #     room_code="AAAA",
#     #     number_of_user=2,
#     #     max_capacity=5,
#     #     last_activity="2023-09-13 10:00:00",
#     #     host_id="123",
#     #     status="waiting",
#     #     room_location="idkwhatisthis",
#     #     room_activity="idkwhatisthis",
#     # )
#     # room.add_user(User("u1", "Alice"))
#     # room.add_user(User("u2", "Bob"))
#     # question1 = Question(
#     #     question_id="q1", question_text="What's your " "favorite color?"
#     # )
#     # question1.add_option(Option(option_id="o1", option_text="Red", current_votes=3))
#     # question1.add_option(Option(option_id="o2", option_text="Blue", current_votes=5))
#     # room.add_question(question1)
#     #
#     # room2 = Room(
#     #     room_id="r2",
#     #     room_code="BBBB",
#     #     number_of_user=2,
#     #     max_capacity=5,
#     #     last_activity="2023-09-13 10:00:00",
#     #     host_id="123",
#     #     status="waiting",
#     #     room_location="idkwhatisthis",
#     #     room_activity="idkwhatisthis",
#     # )
#     # room2.add_user(User("u1", "Alice"))
#     # room2.add_user(User("u2", "Bob"))
#     # question1 = Question(
#     #     question_id="q1", question_text="What's your " "favorite color?"
#     # )
#     # question1.add_option(Option(option_id="o1", option_text="Red", current_votes=3))
#     # question1.add_option(Option(option_id="o2", option_text="Blue", current_votes=5))
#     # room2.add_question(question1)
#     #
#     # mock_redis = Database()
#     # """Test room functions"""
#     # # Test for remove_room_data
#     # mock_redis.remove_room_data(room_id=room.room_id)
#     # mock_redis.remove_room_data(room_id=room2.room_id)
#     # # Check that database is empty
#     # mock_redis.query_all_hash_keys()
#     # # Test store_room_data function
#     # # mock_redis.store_room_data(room_id=room.room_id, room_code=room.room_code, room_data=room)
#     # # mock_redis.store_room_data(
#     # #     room_id=room2.room_id, room_code=room2.room_code, room_data=room2
#     # # )
#     # # # Test for duplicate checking
#     # # mock_redis.store_room_data(
#     # #     room_id=room2.room_id, room_code=room2.room_code, room_data=room2
#     # # )
#     # # # Test for query_room_data function
#     # # print("Querying test:", mock_redis.query_room_data(room.room_id))
#     # #
#     # # """Test for user functions"""
#     # # # Test for get_user function (User Info retrieval)
#     # # print("users:", mock_redis.get_users(room_id=room2.room_id))
#     # # # Test for insert_user function
#     # # new_user = User(user_id="u3", user_name="Charles")
#     # # print("insert_user:", mock_redis.insert_users(room_id=room2.room_id, new_user=new_user))
#     # # print("users:", mock_redis.get_users(room_id=room2.room_id))
#     # # # Test for remove_user function
#     # # print("remove_user:", mock_redis.remove_users(room_id=room2.room_id, user_id="u3"))
#     # # print("users:", mock_redis.get_users(room_id=room2.room_id))
#     # #
#     # # """Test for question functions"""
#     # # # Test for get_question function (Question Info retrieval)
#     # # print("questions:", mock_redis.get_questions(room_id=room2.room_id))
#     # # # Test for insert_question function
#     # # question2 = Question(question_id="q2", question_text="What's is your favorite monster?")
#     # # question2.add_option(Option(option_id="o1", option_text="Ant", current_votes=5))
#     # # question2.add_option(Option(option_id="o2", option_text="Dog", current_votes=1))
#     # # mock_redis.insert_question(room2.room_id, question2)
#     # # print("questions:", mock_redis.get_questions(room_id=room2.room_id))
#     # # """Test for option functions"""
#     # # # Test for get_options function
#     # # print("options:", mock_redis.get_options(room_id=room.room_id, question_id=question1.question_id))
#     # # # Test for update_option function
#     # # new_option = Option(option_id="o1", option_text="Pink", current_votes=10)
#     # # mock_redis.update_options(room_id=room.room_id, question_id=question1.question_id, data=new_option)
#     # # print("options:", mock_redis.get_options(room_id=room.room_id, question_id=question1.question_id))
#     # # """Test for vote functions"""
#     # # # Test for get_vote
#     # # print("votes:", mock_redis.get_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                  option_id=new_option.option_id))
#     # # # Test for increment_vote
#     # # print("increment_vote:", mock_redis.increment_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                                 option_id=new_option.option_id))
#     # # print("votes:", mock_redis.get_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                  option_id=new_option.option_id))
#     # # # Test for decrement_vote
#     # # print("decrement_vote:", mock_redis.decrement_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                                 option_id=new_option.option_id))
#     # # print("votes:", mock_redis.get_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                  option_id=new_option.option_id))
#     # # """Test for update_room_activity_time"""
