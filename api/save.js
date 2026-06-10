const { createClient } = require('redis');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const REDIS_URL = process.env.REDIS_URL || "redis://default:YpxigeuX75iY6FvCubASt2ruLVBKImHF@redis-10083.c92.us-east-1-3.ec2.cloud.redislabs.com:10083";

  try {
    const client = createClient({ url: REDIS_URL });
    client.on('error', (err) => console.log('Redis Client Error', err));
    await client.connect();
    
    const dataToSave = typeof req.body === 'string' ? req.body : JSON.stringify(req.body);

    await client.set('brunazanetti_approvals', dataToSave);
    await client.disconnect();
    
    res.status(200).json({ status: "success" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
};
