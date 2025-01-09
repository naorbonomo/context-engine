# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

- Replace `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked` or `tseslint.configs.strictTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and update the config:

```js
// eslint.config.js
import react from 'eslint-plugin-react'

export default tseslint.config({
  // Set the react version
  settings: { react: { version: '18.3' } },
  plugins: {
    // Add the react plugin
    react,
  },
  rules: {
    // other rules...
    // Enable its recommended rules
    ...react.configs.recommended.rules,
    ...react.configs['jsx-runtime'].rules,
  },
})
```

## Project Structure

Our React + Vite project follows a structured organization:

### CSS Organization
- `App.css`: Global styles and theme variables
- Component-specific CSS files: Located alongside their respective components

### Key Directories
- `/components`: Reusable React components
- `/routes`: Route components and configurations
- `/layouts`: Layout components
- `/assets`: Static assets (images, fonts, etc.)
- `/utils`: Helper functions and utilities
- `/services`: API and service integrations
- `/hooks`: Custom React hooks
- `/constants`: Application constants
- `/types`: TypeScript type definitions (if applicable)

### CSS Guidelines
1. Global styles are maintained in `App.css`
2. Component-specific styles should be in separate CSS files next to their components
3. Use CSS modules for component styling to avoid conflicts
4. Follow BEM naming convention for class names

### Navbar Structure
The navbar component (`/components/Navbar/`) handles main navigation and should be updated when adding new routes.

To add a new route:
1. Create your component in the appropriate directory
2. Add the route to the router configuration
3. Update the Navbar component to include the new navigation link
