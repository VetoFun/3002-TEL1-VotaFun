import Footer from '@/components/dom/Footer';
import './globals.css';
import type { Metadata } from 'next';
import { Comfortaa } from 'next/font/google';

const font = Comfortaa({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'VotaFun',
  description: '',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" data-theme="votafun">
      <body className={`bg-base-100 ${font.className}`}>
        {children}
        <Footer />
      </body>
    </html>
  );
}
