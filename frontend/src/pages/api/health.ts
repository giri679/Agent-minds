import { NextApiRequest, NextApiResponse } from 'next';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ 
    status: 'online',
    message: 'AI Education Agent API is running',
    timestamp: new Date().toISOString()
  });
}
