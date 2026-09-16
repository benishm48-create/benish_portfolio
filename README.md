# Benish — Creative Workspace Portfolio

A custom React + Vite portfolio featuring original Blender scenes, an interactive HP Victus-style desk setup, and a seated music-listening character.

## Start the website

Install Node.js 20.19+ (Node.js 22 LTS is suitable). Extract this ZIP, then open a terminal **inside the folder containing package.json**.

```bash
npm install
npm run dev
```

Open the local URL printed by Vite, usually http://localhost:5173.

For Ubuntu, right-click inside the extracted folder and choose Open in Terminal. For Windows, open the folder in VS Code and choose Terminal > New Terminal.

Do not double-click index.html: the 3D model loader requires an HTTP server.

## Build for hosting

```bash
npm run build
npm run preview
```

The `dist` folder is the static production website. Upload its contents to a static host. The project does not depend on Sites, Cloudflare Workers or an `.openai/hosting.json` file.

## What to edit

| File | Purpose |
| --- | --- |
| `src/data.js` | Personal details, real links, skills, project descriptions and experience |
| `src/main.jsx` | Section content and interactive controls |
| `src/style.css` | Colors, typography, spacing, responsive layout and effects |
| `src/Scene.jsx` | 3D lighting, camera, animation and loading behavior |
| `public/Benish-M-Resume.pdf` | Original supplied resume, linked to Download Resume |
| `public/models/` | Ready-to-use GLB scenes and static fallback images |
| `public/textures/` | Original code-editor and music-interface screen textures |
| `blender/create-scenes.py` | Reproducible Blender scene-generation script |
| `scripts/create-textures.py` | Optional screen texture generator (Python + Pillow) |

The model filenames are `hero-workspace.glb` and `about-workspace.glb`.

## Blender source

Open the provided `.blend` files in Blender 4.3 or newer. Scene objects are named individually: desk, chair, laptop chassis, screen, keyboard keys, lamp, plant and character parts. Textures are packed into the Blender files and GLB assets.

To rebuild the scenes from the project root:

```bash
blender --background --python blender/create-scenes.py
```

This creates both editable `.blend` scenes, both `.glb` exports and transparent PNG renders. The web fallback uses WebP copies; convert regenerated PNGs with:

```bash
python -m pip install Pillow
python scripts/convert-previews.py
```

Blender is only needed to edit or rebuild the 3D assets. It is **not required to run the website**.

## Interactions

- Drag either scene through a full 360° horizontally. Scroll or pinch to zoom; + / − buttons also zoom, with safe bounds.
- Reset buttons restore the camera angle and zoom.
- About's pause button pauses the character and visualizer. There is no audio playback.
- Project cards open accessible detail dialogs; Escape or clicking the backdrop closes them.
- Email button copies the address, with a mailto fallback.
- Resume download, LinkedIn and GitHub use details from the supplied PDF.
- Mobile navigation opens via the menu button.

## Content and limitations

- The character is an original stylized avatar, not a likeness based on a photograph.
- HP Victus and Spotify are descriptive brand references; this is not an official branded product or an authenticated Spotify integration.
- The Spotify-style screen is a silent visual mockup with fictional track labels.
- Project interface previews are clearly labeled illustrative concepts, not screenshots of the actual applications. The supplied boutique demo link is included but third-party uptime is outside this project's control.
- No project-specific repository URLs were supplied; the actual GitHub profile is linked instead of invented repositories.
- Work titles and dates follow the uploaded resume. Update `src/data.js` as your role changes.
- WebGL2-capable browsers display the live 3D scenes. Static rendered fallbacks remain available when WebGL is unsupported.
- Reduced-motion preferences stop automatic animation; offscreen scenes pause rendering.
- Fonts and 3D assets are bundled locally. No external font/CDN requests are needed at runtime.

## Credits

Original scene models, screen textures, layout and implementation created for Benish M. Inter is distributed through @fontsource/inter under its included SIL Open Font License. Lucide icons use the ISC license. Dependency licenses are available in their installed packages.

## Updated models

Detailed stylized assets: tilted laptop lid, hinges, key legends, cooling vents, USB recesses, speaker grilles, chair piping, lumbar support, shoe laces and articulated resting fingers. About uses connected sculpted clothing surfaces, a reclined torso, attached shoulders and hands, a downcast expression and slow head movement. Materials include procedural walnut and fabric bump detail in Blender; procedural shader detail is not baked into the web GLBs. This is a stylized scene, not photorealistic character sculpting.
