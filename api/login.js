module.exports = (req, res) => {
  if (req.method === 'POST') {
    const { username, password } = req.body || {};
    
    // Verificação de usuário e senha
    if (username === 'bruna' && password === 'bruna2026') {
      res.status(200).json({ success: true, username, token: "fake-jwt-token" });
    } else {
      res.status(401).json({ success: false, message: "Usuário ou senha incorretos." });
    }
  } else {
    res.status(405).json({ error: "Method not allowed" });
  }
};
