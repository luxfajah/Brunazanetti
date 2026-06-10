const { createClient } = require('redis');

module.exports = async (req, res) => {
  const REDIS_URL = process.env.REDIS_URL || "redis://default:YpxigeuX75iY6FvCubASt2ruLVBKImHF@redis-10083.c92.us-east-1-3.ec2.cloud.redislabs.com:10083";
  
  try {
    const client = createClient({ url: REDIS_URL });
    client.on('error', (err) => console.log('Redis Client Error', err));
    await client.connect();
    
    const data = await client.get('brunazanetti_approvals');
    await client.disconnect();
    
    if (data) {
      res.status(200).json(JSON.parse(data));
    } else {
      res.status(200).json({});
    }
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
};
