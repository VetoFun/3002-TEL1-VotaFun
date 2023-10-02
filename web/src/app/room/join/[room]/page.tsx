'use client';
import { motion } from 'framer-motion';
import { Loader } from '@/components/common/Loader';
import { UserNameInput } from '@/app/room/join/[room]/components/UserNameInput';

interface DashLineProps {
  width: string;
  x: string;
  y: string;

  color?: string;
  speed?: number;
  delay?: number;
}

const DashLine = ({ x, y, width, color = 'bg-neutral', speed = 1.5, delay = 0 }: DashLineProps) => {
  return (
    <motion.span
      className={`absolute inline-block h-1 ${width} ${x} ${y} ${color}`}
      animate={{
        x: ['110vw', '-110vw'],
      }}
      transition={{ duration: speed, delay: delay, repeat: Infinity, ease: [0.17, 0.67, 0.83, 0.67] }}
    />
  );
};

export default function JoinRoomPage() {
  return (
    <main className="h-screen w-screen">
      <div className="relative left-1/2 top-1/2 flex w-fit -translate-x-1/2 -translate-y-1/3 flex-col gap-2">
        <div className="mx-auto mb-16">
          <Loader />
        </div>
        <UserNameInput />
      </div>
      <motion.div className="pointer-events-none fixed left-0 top-1/2 h-1/4 w-screen -translate-y-1/2">
        <DashLine x="left-0" y="top-1/2" width="w-16" color="bg-primary" />
        <DashLine x="left-0" y="top-2/3" width="w-10" color="bg-info" speed={3} delay={1} />
        <DashLine x="left-0" y="top-3/4" width="w-18" color="bg-error" speed={1} delay={2} />
        <DashLine x="left-0" y="top-1/4" width="w-12" color="bg-success" speed={2} delay={3} />
        <DashLine x="left-0" y="top-1/5" width="w-16" color="bg-warning" speed={1} delay={4} />
        <DashLine x="left-0" y="top-1/6" width="w-16" color="bg-accent" speed={3} delay={5} />
        <DashLine x="left-0" y="top-1/7" width="w-16" color="bg-neutral" speed={2} delay={6} />
      </motion.div>
    </main>
  );
}
