/*
/!** @type {import('tailwindcss').Config} *!/
module.exports = {
  mode: "jit", // JIT modunu etkinleştir
  purge: ["./spring-frontend/src/!**!/!*.{js,jsx,ts,tsx}"], // React bileşenlerini temizle
  theme: {
    extend: {
      colors: {
        /!*primary: "#2563EB",
        secondary: "#1E40AF",
        accent: "#F97316",*!/
      },
    },
  },
  safelist: [
    "text-red-500", 
    "bg-blue-500",
    "bg-red-500",
    "text-white",
    "text-gray-900",
    "text-green-500",
    "text-yellow-500"
  ], // Tailwind’in temizlememesi gereken sınıflar
  plugins: [],
};
*/

module.exports = {

  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
    ],
  },
  // content: ["./spring-frontend/src/**/*.{js,jsx,ts,tsx}"],
  content: [
     "./spring-frontend/src/**/*.{js,jsx,ts,tsx,html,css}",
    "./spring-frontend/src/index.js",
    "./spring-frontend/src/App.js",
    "./spring-frontend/src/pages/Auth.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

