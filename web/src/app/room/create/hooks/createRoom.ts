import { Room } from '@/types/Room';

function random(min: number, max: number): number {
  return Math.random() * (max - min) + min;
}

const createRoom = (): Room => {
  // [todo] call endpoint to createRoom

  return { id: random(1000000, 5000000).toFixed(0).toString(), activity: '', location: '', users: [], host: null };
};

export { createRoom };
