const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  try {
    const dbPath = path.join(process.cwd(), 'database.json');
    const dbContent = fs.readFileSync(dbPath, 'utf8');
    res.status(200).json(JSON.parse(dbContent));
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
