import React, { useState } from "react";
import { Box, Button, TextField, Typography, Paper, Link } from "@mui/material";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { CircularProgress } from "@mui/material";
import { AccountTree } from "@mui/icons-material";

const Login: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return toast.error("Email or mobile is required");
    if (!password) return toast.error("Password is required");
    setLoading(true);
    try {
      await login(email, password);
      toast.success("Login successful");
      // replace so login page isn't kept in history
      navigate("/record/batch-list", { replace: true });
    } catch (err: any) {
      toast.error(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ mt: 8, display: "flex", justifyContent: "center" }}>
      <Paper
        sx={{ p: 3, width: { xs: "95%", sm: "80%", md: 520 } }}
        elevation={3}
      >
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 1,
            mb: 2,
          }}
        >
          <AccountTree fontSize="medium" sx={{ color: "#cc6600" }} />
          <Typography
            variant="h6"
            sx={{
              fontFamily: "'Oswald', sans-serif",
              fontWeight: 700,
              fontSize: "1.1rem",
              letterSpacing: 1.2,
              textTransform: "uppercase",
              background: "linear-gradient(90deg, #333333, #555555)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              textShadow: "0.5px 0.5px 1px rgba(0,0,0,0.3)",
            }}
          >
            Klassic Foods ERP
          </Typography>
        </Box>
        <Box sx={{ borderBottom: "2px solid #eee", mb: 2 }} />
        <Typography
          variant="body2"
          align="center"
          sx={{ color: "#666", mb: 1 }}
        >
          Sign in to continue
        </Typography>

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            label="Email or Mobile"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            fullWidth
            margin="normal"
          />

          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
            margin="normal"
          />

          <Box
            mt={2}
            display="flex"
            justifyContent="space-between"
            alignItems="center"
          >
            <Button variant="outlined" onClick={() => navigate(-1)}>
              Cancel
            </Button>
            <Box>
              <Link href="/auth/signup" sx={{ mr: 2 }}>
                Not a member? Sign up
              </Link>
              <Button
                type="submit"
                variant="contained"
                disabled={loading}
                sx={{
                  "&:hover": {
                    backgroundColor: "#b35400",
                  },
                }}
              >
                {loading ? (
                  <CircularProgress size={24} color="inherit" />
                ) : (
                  "Login"
                )}
              </Button>
            </Box>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default Login;
