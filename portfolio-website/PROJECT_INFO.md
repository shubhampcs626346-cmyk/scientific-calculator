# 🚀 Interactive Portfolio Website

An impressive, modern portfolio website built with Next.js 14, TypeScript, and Tailwind CSS.

## ✨ Features

### 🎨 Interactive Design
- **Mouse-tracking gradient effects** - Background responds to cursor movement
- **Smooth scroll animations** - Parallax effects on hero section
- **Animated skill bars** - Progress bars with smooth transitions
- **Hover effects** - Interactive cards and buttons with scale transforms
- **Gradient backgrounds** - Beautiful purple/pink gradient theme

### 📱 Responsive Layout
- Fully responsive design that works on all devices
- Mobile-friendly navigation
- Adaptive grid layouts

### 🎯 Key Sections
1. **Hero Section** - Eye-catching introduction with animated gradient text
2. **About Section** - Personal introduction with statistics cards
3. **Projects Section** - Featured projects with hover effects
4. **Skills Section** - Animated progress bars showing expertise levels
5. **Contact Section** - Beautiful contact form
6. **Showcase Page** - Separate page with filterable project gallery

## 🛠️ Technologies Used

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **React Hooks** - useState, useEffect for interactivity

## 🚀 Getting Started

### To view the website:

```bash
cd portfolio-website
npm run dev
```

Then open your browser and visit: `http://localhost:3000`

### To build for production:

```bash
npm run build
npm start
```

## 📂 Project Structure

```
portfolio-website/
├── app/
│   ├── page.tsx          # Main homepage with all sections
│   ├── showcase/
│   │   └── page.tsx      # Showcase page with project gallery
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── public/               # Static assets
└── package.json          # Dependencies
```

## 🎨 Design Highlights

- **Color Scheme**: Purple and pink gradients on dark background
- **Typography**: Clean, modern fonts with proper hierarchy
- **Animations**: Smooth transitions and hover effects
- **Layout**: Centered content with maximum width constraints
- **Spacing**: Generous padding and margins for breathing room

## 📄 Pages

### Home Page (`/`)
- Navigation bar with smooth scroll links
- Hero section with animated gradient text
- About section with stats
- Featured projects grid
- Skills with progress bars
- Contact form
- Footer with social links

### Showcase Page (`/showcase`)
- Filterable project gallery (All, Web, Mobile, Design)
- Animated project cards
- Category filtering
- Call-to-action section

## 🎯 Interactive Features

1. **Mouse Tracking**: Background gradient follows cursor
2. **Scroll Effects**: Hero section has parallax effect
3. **Hover Animations**: Cards scale and change colors on hover
4. **Smooth Scrolling**: Navigation links scroll smoothly to sections
5. **Tab Filtering**: Showcase page has interactive category filters

## 💡 Customization Tips

To customize this portfolio for your needs:

1. **Update Content**: Edit the text in `app/page.tsx`
2. **Change Colors**: Modify gradient classes (from-purple-500, to-pink-500, etc.)
3. **Add Projects**: Update the `projects` array with your own projects
4. **Update Skills**: Modify the `skills` array with your expertise
5. **Add Images**: Place images in `public/` folder and reference them

## 🌟 Perfect For

- Showcasing your work to potential clients
- Presenting in class or meetings
- Job applications and interviews
- Personal branding
- Portfolio presentations

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

---

**Built with ❤️ using Next.js and Tailwind CSS**
