import './globals.css';

export const metadata = {
  title: 'AI Interview Platform',
  description: 'Mock interviews with Python backend',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}