# Flipside

Flipside is a **single-file, local-first flashcard application** designed for speed, simplicity, and privacy. It runs entirely in the browser without a backend server, storing all data on your device.

## Overview

Flipside provides a modern, distraction-free interface for creating and studying flashcards. It supports rich text editing with Markdown and LaTeX (via KaTeX) for math and chemistry, making it suitable for a wide range of subjects. Because it is a single HTML file, it is extremely portable and can be run offline once the initial dependencies are cached (or if you download them).

## Features

*   **Local-First:** All data is stored in your browser's `localStorage`. No accounts, no logins, no tracking.
*   **Rich Editing:** Support for **Markdown** and **LaTeX** (Math/Chemistry symbols).
*   **Study Modes:**
    *   **Flashcards:** Standard flip-to-reveal mode.
    *   **Type Term/Definition:** Practice by typing the answer for better retention.
*   **Smart Sorting:** Option to prioritize cards based on your study history (strength).
*   **Sharing:** Share decks instantly via a unique URL. The deck data is compressed and embedded in the link itself.
*   **Import/Export:**
    *   Export your entire library to a JSON file for backup.
    *   Import decks from text/CSV (e.g., from spreadsheets).
    *   Restore backups by merging or replacing your current library.
*   **Statistics:** detailed session tracking (time, accuracy, cards studied).

## Project Structure

The project is intentionally minimal:

```
.
├── index.html      # The entire application (HTML, CSS, JS)
├── favicon.svg     # App icon
└── README.md       # Project documentation
```

## Technical Architecture

Flipside is built as a **Single Page Application (SPA)** contained within a single HTML file. It uses `Babel Standalone` to compile React/JSX in the browser at runtime, avoiding the need for a complex build step (like Webpack or Vite) for development or simple deployment.

### Libraries & Dependencies

All libraries are loaded via CDN.

| Library | Version | Purpose |
| :--- | :--- | :--- |
| **React** | 18.x | UI Library (Core component structure) |
| **ReactDOM** | 18.x | DOM rendering for React |
| **Babel Standalone** | - | Transpiles JSX/ES6+ to browser-compatible JavaScript on the fly |
| **Tailwind CSS** | (Play CDN) | Utility-first CSS framework for styling |
| **FontAwesome** | 6.4.0 | UI Icons |
| **LZ-String** | 1.4.4 | Compression algorithm for generating shareable URLs |
| **KaTeX** | 0.16.9 | Rendering Math and Chemistry equations (LaTeX) |
| **Emoji Picker Element** | ^1 | Native web component for the emoji picker |

### Data Storage

Data persistence is handled via the browser's `localStorage` API.

*   **Key:** `flipside_v1`
*   **Format:** A JSON string containing:
    *   `decks`: Array of deck objects (each with an `id`, `title`, and list of `cards`).
    *   `sessions`: Array of study session history objects.
    *   `lastBackup`: Timestamp of the last export.

A secondary key `flipside_visited` is used to track if the welcome modal has been shown.

### URL Compression & Sharing

One of the unique features of Flipside is its serverless sharing capability.

1.  **Compression:** When you click "Share", the application takes the specific deck object and converts it to a JSON string.
2.  **Encoding:** This JSON string is compressed using `LZString.compressToEncodedURIComponent()`.
3.  **Link Generation:** The compressed string is appended to the current URL as a query parameter: `?share=<compressed_string>`.

When a user opens this link:
1.  The app checks for the `share` query parameter on load.
2.  It attempts to decompress the string using `LZString.decompressFromEncodedURIComponent()`.
3.  If valid, the deck is parsed and imported into the user's local library.

### Import/Export Format

**JSON Backups:**
The export file is a raw dump of the `flipside_v1` state. It allows users to migrate their data between devices or browsers manually.

**Text/CSV Import:**
The editor supports pasting data from spreadsheets. It detects tab-separated or comma-separated values.
*   Format: `Term <tab> Definition` or `Term, Definition`
*   Quotes handling: A helper function `stripQuotes` removes surrounding quotes often added by Excel/CSV exports and resolves escaped quotes (`""`).

## Getting Started

### Running Locally

Since there is no build step, you can run the application simply by serving the directory.

**Option 1: Python Simple Server**
If you have Python installed:
```bash
python3 -m http.server
# Open http://localhost:8000 in your browser
```

**Option 2: Open File**
You can often just open `index.html` directly in your browser, though some features (like clipboard access or certain emoji picker internals) may behave differently depending on browser security policies for `file://` protocols.

### Development

To make changes:
1.  Open `index.html` in your favorite code editor.
2.  Edit the code within the `<script type="text/babel">` block.
3.  Refresh your browser to see changes.

## Contributing

Contributions are welcome! Since this is a single-file project, please keep the code organized within the main `App` component and its sub-components.

1.  Ensure you do not break the "single-file" constraint (do not split code into separate `.js` files unless you are proposing a build system migration, which is currently out of scope).
2.  Test that import/export and sharing continue to work, as these rely heavily on the specific data structure.
