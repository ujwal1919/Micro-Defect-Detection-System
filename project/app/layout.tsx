import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from './providers';
import { TooltipProvider } from '@/components/ui/tooltip';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'PCB Defect Analysis',
  description: 'AI-Powered PCB Defect Detection System',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} min-h-screen bg-[#1a1a1a]`}>
        <div className="fixed inset-0 bg-gradient-to-br from-purple-500/10 via-transparent to-purple-700/10" />
        <Providers>
          <TooltipProvider>
            {children}
          </TooltipProvider>
        </Providers>
      </body>
    </html>
  );
}