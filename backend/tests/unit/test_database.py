# import pytest
# from src.database.Database import Database
# from src.database.Room import Room
# from src.database.Question import Question
# from src.database.User import User
# from src.database.Option import Option
#
#
# def create_test_room():
#     # Test for remove_room_data
#     test_room = Room(
#         room_id="r1",
#         room_code="AAAA",
#         number_of_user=2,
#         max_capacity=5,
#         last_activity="2023-09-13 10:00:00",
#         host_id="123",
#         status="waiting",
#         room_location="idkwhatisthis",
#         room_activity="idkwhatisthis",
#     )
#     test_room.add_user(User("u1", "Alice"))
#     test_room.add_user(User("u2", "Bob"))
#     question1 = Question(
#         question_id="q1", question_text="What's your " "favorite color?"
#     )
#     question1.add_option(Option(option_id="o1", option_text="Red", current_votes=3))
#     question1.add_option(Option(option_id="o2", option_text="Blue", current_votes=5))
#     test_room.add_question(question1)
#     return test_room
#
#
# def reset_db(test_db: Database):
#     # confirmation = input("Resetting the database will remove all data. Continue? (y/n): ")
#     # if confirmation.strip().lower() == 'y':
#     hkeys = test_db.query_all_hash_keys()
#     if hkeys is not None and len(hkeys) > 0:
#         for hkey in hkeys:
#             test_db.remove_room_data(hkey)
#
#
# # Create a fixture for the database instance
# @pytest.fixture
# def test_db():
#     test_db = Database()
#     with test_db.r as conn:
#         # Ensure the connection is established
#         assert conn
#     return test_db
#
#
# def test_does_room_id_exist(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#     # Test that a non-existing room ID returns False
#     assert not test_db.does_room_id_exist("test_false_case")
#
#     # Store a room in the database
#     test_db.store_room_data(test_room.room_id, "Test Code", test_room)
#
#     # Test that the existing room ID returns True
#     assert test_db.does_room_id_exist(test_room.room_id)
#
#
# def test_query_room_data(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#
#     # Store room data in the database
#     test_db.store_room_data(test_room.room_id, "Test Code", test_room)
#
#     # Test querying room data
#     retrieved_data = test_db.query_room_data(test_room.room_id)
#
#     # Check that the retrieved data matches the stored data
#     assert retrieved_data == test_room
#
#
# def test_store_room_data(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#     # Test storing room data
#     result = test_db.store_room_data(test_room.room_id, test_room.room_code, test_room)
#
#     # Check that the operation was successful
#     assert result
#
#
# def test_remove_room_data(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#
#     # Store a room in the database
#     test_db.store_room_data(test_room.room_id, "Test Code", test_room)
#
#     # Test removing room data
#     result = test_db.remove_room_data(test_room.room_id)
#
#     # Check that the operation was successful
#     assert result is True
#
#
# def test_get_users(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#
#     # Store a room in the database
#     test_db.store_room_data(test_room.room_id, "Test Code", test_room)
#
#     # Test getting users
#     users = test_db.get_users(test_room.room_id)
#
#     # Check that the user is in the list of users
#     assert len(users) == len(test_room.users)
#     assert users[0]["user_id"] == "u1"
#
#
# def test_insert_users(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#
#     # Store a room in the database
#     test_db.store_room_data(test_room.room_id, "Test Code", test_room)
#     test_user = User(user_id="u3", user_name="Charles")
#
#     # Test inserting a user
#     result = test_db.insert_users(test_room.room_id, test_user)
#
#     # Check that the operation was successful
#     assert result is True
#
#
# def test_remove_users(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#
#     # Store a room in the database
#     test_db.store_room_data(test_room.room_id, "Test Code", test_room)
#
#     result = test_db.remove_users(test_room.room_id, "u2")
#
#     # Check that the operation was successful
#     assert result is True
#
#
# def test_get_questions(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#     test_db.store_room_data(test_room.room_id, test_room.room_code, test_room)
#     questions = test_db.get_questions(test_room.room_id)
#     assert len(questions) == 1
#     assert questions[0]["question_id"] == "q1"
#
#
# def test_insert_question(test_db):
#     reset_db(test_db)
#     test_room = create_test_room()
#     test_db.store_room_data(test_room.room_id, test_room.room_code, test_room)
#     question = Question(
#         question_id="q3",
#         question_text="What's your favorite animal?",
#         options=[Option("o1", "dinosaur", 3)],
#     )
#
#     # Test inserting a question
#     result = test_db.insert_question(test_room.room_id, question)
#
#     # Check that the operation was successful
#     assert result is True
#
#
# # def test_get_options(test_db):
# #     reset_db(test_db)
# #     test_room = create_test_room()
# #     test_db.store_room_data(test_room.room_id, test_room.room_code, test_room)
# #     options = test_db.get_options(test_room.room_id, test_room.questions[0]["q1"])
# #
# #     # Check that the option is in the list of options
# #     assert len(options) == 1
# #     assert options[0]["option_id"] == "o1"
#
#
# # def test_update_options(test_db):
# #     room_id = "test_room"
# #     question_id = "q1"
# #     option = Option(option_id="o1", option_text="Blue", current_votes=5)
# #
# #     # Test updating options
# #     result = test_db.update_options(room_id, question_id, option)
# #
# #     # Check that the operation was successful
# #     assert result is True
# #
# #
# # def test_get_vote(test_db):
# #     room_id = "test_room"
# #     question_id = "q1"
# #     option_id = "o1"
# #     option = Option(option_id=option_id, option_text="Green", current_votes=3)
# #     test_db.store_single_field(room_id, "questions", [{"question_id": question_id, "options": [option.to_dict()]}],
# #                                True)
# #
# #     # Test getting the vote count
# #     vote_count = test_db.get_vote(room_id, question_id, option_id)
# #
# #     # Check that the vote count matches the stored value
# #     assert vote_count == 3
# #
# #
# # def test_increment_vote(test_db):
# #     room_id = "test_room"
# #     question_id = "q1"
# #     option_id = "o1"
# #
# #     # Test incrementing the vote count
# #     result = test_db.increment_vote(room_id, question_id, option_id)
# #
# #     # Check that the operation was successful
# #     assert result is True
# #
# #
# # def test_decrement_vote(test_db):
# #     room_id = "test_room"
# #     question_id = "q1"
# #     option_id = "o1"
# #
# #     # Test decrementing the vote count
# #     result = test_db.decrement_vote(room_id, question_id, option_id)
# #
# #     # Check that the operation was successful
# #     assert result is True
# #
# #
# # def test_update_room_activity_time(test_db):
# #     room_id = "test_room"
# #     new_activity_time = datetime.now()
# #
# #     # Test updating the room's activity time
# #     result = test_db.update_room_activity_time(room_id, new_activity_time)
# #
# #     # Check that the operation was successful
# #     assert result is True
# #
# #
# # def test_get_room_location(test_db):
# #     room_id = "test_room"
# #     location = "Living Room"
# #     test_db.store_single_field(room_id, "room_location", location)
# #
# #     # Test getting the room's location
# #     retrieved_location = test_db.get_room_location(room_id)
# #
# #     # Check that the retrieved location matches the stored location
# #     assert retrieved_location == location
# #
# #
# # def test_update_room_location(test_db):
# #     room_id = "test_room"
# #     new_location = "Bedroom"
# #
# #     # Test updating the room's location
# #     result = test_db.update_room_location(room_id, new_location)
# #
# #     # Check that the operation was successful
# #     assert result is True
# #
# #
# # def test_get_room_activity(test_db):
# #     room_id = "test_room"
# #     activity = "Watching TV"
# #     test_db.store_single_field(room_id, "room_activity", activity)
# #
# #     # Test getting the room's activity
# #     retrieved_activity = test_db.get_room_activity(room_id)
# #
# #     # Check that the retrieved activity matches the stored activity
# #     assert retrieved_activity == activity
# #
# #
# # def test_update_room_activity(test_db):
# #     room_id = "test_room"
# #     new_activity = "Reading"
# #
# #     # Test updating the room's activity
# #     result = test_db.update_room_activity(room_id, new_activity)
# #
# #     # Check that the operation was successful
# #     assert result is True
#
#
# def test_query_all_hash_keys(test_db):
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
#     # test_db = Database()
#     # """Test room functions"""
#     # # Test for remove_room_data
#     # test_db.remove_room_data(room_id=room.room_id)
#     # test_db.remove_room_data(room_id=room2.room_id)
#     # # Check that database is empty
#     # test_db.query_all_hash_keys()
#     # # Test store_room_data function
#     # # test_db.store_room_data(room_id=room.room_id, room_code=room.room_code, room_data=room)
#     # # test_db.store_room_data(
#     # #     room_id=room2.room_id, room_code=room2.room_code, room_data=room2
#     # # )
#     # # # Test for duplicate checking
#     # # test_db.store_room_data(
#     # #     room_id=room2.room_id, room_code=room2.room_code, room_data=room2
#     # # )
#     # # # Test for query_room_data function
#     # # print("Querying test:", test_db.query_room_data(room.room_id))
#     # #
#     # # """Test for user functions"""
#     # # # Test for get_user function (User Info retrieval)
#     # # print("users:", test_db.get_users(room_id=room2.room_id))
#     # # # Test for insert_user function
#     # # new_user = User(user_id="u3", user_name="Charles")
#     # # print("insert_user:", test_db.insert_users(room_id=room2.room_id, new_user=new_user))
#     # # print("users:", test_db.get_users(room_id=room2.room_id))
#     # # # Test for remove_user function
#     # # print("remove_user:", test_db.remove_users(room_id=room2.room_id, user_id="u3"))
#     # # print("users:", test_db.get_users(room_id=room2.room_id))
#     # #
#     # # """Test for question functions"""
#     # # # Test for get_question function (Question Info retrieval)
#     # # print("questions:", test_db.get_questions(room_id=room2.room_id))
#     # # # Test for insert_question function
#     # # question2 = Question(question_id="q2", question_text="What's is your favorite monster?")
#     # # question2.add_option(Option(option_id="o1", option_text="Ant", current_votes=5))
#     # # question2.add_option(Option(option_id="o2", option_text="Dog", current_votes=1))
#     # # test_db.insert_question(room2.room_id, question2)
#     # # print("questions:", test_db.get_questions(room_id=room2.room_id))
#     # # """Test for option functions"""
#     # # # Test for get_options function
#     # # print("options:", test_db.get_options(room_id=room.room_id, question_id=question1.question_id))
#     # # # Test for update_option function
#     # # new_option = Option(option_id="o1", option_text="Pink", current_votes=10)
#     # # test_db.update_options(room_id=room.room_id, question_id=question1.question_id, data=new_option)
#     # # print("options:", test_db.get_options(room_id=room.room_id, question_id=question1.question_id))
#     # # """Test for vote functions"""
#     # # # Test for get_vote
#     # # print("votes:", test_db.get_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                  option_id=new_option.option_id))
#     # # # Test for increment_vote
#     # # print("increment_vote:", test_db.increment_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                                 option_id=new_option.option_id))
#     # # print("votes:", test_db.get_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                  option_id=new_option.option_id))
#     # # # Test for decrement_vote
#     # # print("decrement_vote:", test_db.decrement_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                                 option_id=new_option.option_id))
#     # # print("votes:", test_db.get_vote(room_id=room.room_id, question_id=question1.question_id,
#     # #                                  option_id=new_option.option_id))
#     # # """Test for update_room_activity_time"""
