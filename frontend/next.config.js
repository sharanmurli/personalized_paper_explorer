/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    // not used by the code anymore, but harmless to leave
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || "",
  },
  async rewrites() {
    return [
      {
        // Browser calls http://localhost:3000/api/... and Next proxies to the backend container
        source: "/api/:path*",
        destination: "http://backend:8001/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
