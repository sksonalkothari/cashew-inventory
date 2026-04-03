import React, { useState } from "react";
import { Box, Button, TextField, Typography, Paper, Link } from "@mui/material";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { AccountTree } from "@mui/icons-material";

const Signup: React.FC = () => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();
  const { signup } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name.trim()) return toast.error("Name is required");
    if (!email.trim()) return toast.error("Email is required");
    if (!password) return toast.error("Password is required");
    if (password !== confirmPassword)
      return toast.error("Passwords do not match");

    try {
      await signup({ name, email, password });
      toast.success("Signup successful — please login");
      navigate("/auth/login");
    } catch (err: any) {
      toast.error(err.message || "Signup failed");
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
          Create your Klassic Foods ERP account
        </Typography>

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth
            margin="normal"
          />

          <TextField
            label="Email"
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

          <TextField
            label="Confirm password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            fullWidth
            margin="normal"
          />

          <Box mt={2} display="flex" justifyContent="space-between">
            <Button variant="outlined" onClick={() => navigate(-1)}>
              Cancel
            </Button>
            <Button type="submit" variant="contained">
              Sign up
            </Button>
          </Box>
          <Box mt={2} textAlign="center">
            <Link href="/auth/login">Already have an account? Log in</Link>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default Signup;
