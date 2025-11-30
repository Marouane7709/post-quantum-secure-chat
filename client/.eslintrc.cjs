module.exports = {
  root: true,
  env: { browser: true, es2022: true },
  extends: ["eslint:recommended", "plugin:react/recommended", "plugin:@typescript-eslint/recommended"],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["react-refresh"],
  rules: {
    "react-refresh/only-export-components": "warn",
    "react/react-in-jsx-scope": "off",
  },
  settings: {
    react: { version: "detect" },
  },
};

