"use client"

import { useState } from "react";
import { Card, Input, Button, Alert, Form} from "@heroui/react";
import { getBaseUrl } from "@/config/base_url"

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setToken(null);

    try {
      // console.log(`URL link: ${getBaseUrl()}`)

      const res = await fetch(`${getBaseUrl()}/auth/token/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (!res.ok) {
        const errData = await res.json();
        setError(errData.detail || "Login failed");
        return;
      }

      const data = await res.json();
      setToken(data.access_token);
    } catch (err) {
      setError("Network error");
    }
  };

  return (
    <div className="flex justify-center items-center w-full">
      <Card className="max-w-md w-full p-6 shadow-lg">
        <h2 className="text-2xl font-bold mb-4 text-center">Login</h2>
        <Form onSubmit={handleSubmit}>
          <Input
            label="Email"
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full"
          />
          <Input
            label="Password"
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full"
          />
          <Button type="submit" color="primary">
            Login
          </Button>
        </Form>
        {token && (
          <Alert color="success" description={token} title="Access Token:" />
        )}
        {error && (
          <Alert color="danger" description={token} title="Error:" />
        )}
      </Card>
    </div>
  );
}
