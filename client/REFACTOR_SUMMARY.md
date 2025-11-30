# Frontend Refactor Summary

## Overview
The frontend has been refactored from a single-page app with three cards into a multi-page routed application using React Router v6.

## File Structure

### New Files Created

```
client/src/
├── types.ts                    # Shared TypeScript interfaces
├── contexts/
│   └── AuthContext.tsx         # Auth state management (token, user, logout)
├── components/
│   └── RequireAuth.tsx         # Auth guard component
├── layouts/
│   ├── AuthLayout.tsx          # Layout for /auth/* pages
│   └── AppLayout.tsx           # Layout for /app pages
└── pages/
    ├── LoginPage.tsx           # Login form page
    ├── RegisterPage.tsx        # Registration form page
    └── DashboardPage.tsx       # Main app page (send message + inbox)
```

### Modified Files

- `src/App.tsx` - Now defines routes and wraps with AuthProvider
- `src/main.tsx` - Unchanged (still renders App)
- `src/index.css` - Completely rewritten with new layout styles
- `package.json` - Added `react-router-dom` dependency

## Route Structure

- `/` → Redirects to `/auth/login`
- `/auth/login` → LoginPage (wrapped in AuthLayout)
- `/auth/register` → RegisterPage (wrapped in AuthLayout)
- `/app` → DashboardPage (wrapped in AppLayout, protected by RequireAuth)

## Auth Logic Location

### Registration
- **Location**: `src/pages/RegisterPage.tsx`
- **Endpoint**: `POST /auth/register`
- **Flow**: 
  1. User submits form
  2. API call to register endpoint
  3. On success, shows key bundle and redirects to `/auth/login` after 2 seconds

### Login
- **Location**: `src/pages/LoginPage.tsx`
- **Endpoint**: `POST /auth/login`
- **Flow**:
  1. User submits credentials
  2. API call to login endpoint
  3. Token stored in localStorage via `AuthContext.setToken()`
  4. Navigates to `/app`

### Auth State Management
- **Location**: `src/contexts/AuthContext.tsx`
- **Features**:
  - Token persistence in localStorage
  - Auto-fetch current user on token change
  - Logout function
  - Available via `useAuth()` hook throughout app

### Auth Guard
- **Location**: `src/components/RequireAuth.tsx`
- **Behavior**: Redirects to `/auth/login` if no token found

## Message Functionality Location

### Sending Messages
- **Location**: `src/pages/DashboardPage.tsx` (left card)
- **Endpoint**: `POST /messages`
- **Features**:
  - Recipient dropdown (fetches from `/users`)
  - Message textarea
  - Encrypt & Send button
  - Status messages

### Inbox & Decryption
- **Location**: `src/pages/DashboardPage.tsx` (right card)
- **Endpoints**: 
  - `GET /messages/inbox` - Fetch messages
  - `POST /messages/{id}/decrypt` - Decrypt message
- **Features**:
  - Auto-refresh every 5 seconds
  - Decrypt button per message
  - Shows plaintext after decryption

## Future UI Extensions

### Adding Conversation View
To add a conversation view inside `/app`:

1. Create `src/pages/ConversationPage.tsx`
2. Add route in `App.tsx`:
   ```tsx
   <Route path="conversation/:userId" element={<ConversationPage />} />
   ```
3. Access via `/app/conversation/123` (where 123 is user ID)

### Adding Message List Component
Create `src/components/MessageList.tsx` and import into `DashboardPage.tsx`:

```tsx
// In DashboardPage.tsx
import { MessageList } from "../components/MessageList";

// Replace inbox rendering with:
<MessageList messages={inbox} onDecrypt={decryptMessage} decryptions={decryptions} />
```

## Design System

### Colors
- Primary gradient: `#667eea` → `#764ba2` → `#f093fb`
- Background: Full-screen gradient on auth pages, same on app pages
- Cards: White with backdrop blur and subtle shadows

### Typography
- Font: Inter (system fallbacks)
- Headings: Bold, gradient text for titles
- Body: `#64748b` for secondary text

### Components
- **Buttons**: Pill-shaped, gradient background, hover effects
- **Inputs**: Rounded corners, blue focus ring, consistent padding
- **Cards**: White background, rounded corners, subtle shadows

## Responsive Design

- Mobile: Stacks dashboard cards vertically
- Tablet: 2-column grid for dashboard
- Desktop: Full layout with max-width 1120px

## Testing the Refactor

1. Start backend: `cd server && uvicorn app.main:app --reload`
2. Start frontend: `cd client && npm run dev`
3. Navigate to `http://localhost:5173`
4. Should redirect to `/auth/login`
5. Test registration → redirects to login
6. Test login → navigates to `/app`
7. Test sending message → works as before
8. Test inbox decryption → works as before

## Breaking Changes

- Old single-page URL structure is gone
- All functionality preserved, just reorganized
- Token storage moved to localStorage (was in component state before)

