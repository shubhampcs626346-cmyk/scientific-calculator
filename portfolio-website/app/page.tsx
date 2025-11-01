"use client"

import { useState, useEffect } from 'react'
import Link from 'next/link'

export default function Home() {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const [scrollY, setScrollY] = useState(0)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }

    const handleScroll = () => {
      setScrollY(window.scrollY)
    }

    window.addEventListener('mousemove', handleMouseMove)
    window.addEventListener('scroll', handleScroll)

    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  const projects = [
    { title: "E-Commerce Platform", desc: "Full-stack shopping experience", color: "from-purple-500 to-pink-500" },
    { title: "AI Dashboard", desc: "Real-time analytics & insights", color: "from-blue-500 to-cyan-500" },
    { title: "Social Network", desc: "Connect & share moments", color: "from-green-500 to-emerald-500" },
    { title: "Crypto Tracker", desc: "Monitor digital assets", color: "from-orange-500 to-red-500" },
  ]

  const skills = [
    { name: "React & Next.js", level: 95 },
    { name: "TypeScript", level: 90 },
    { name: "Node.js", level: 85 },
    { name: "UI/UX Design", level: 88 },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Animated Background */}
      <div 
        className="fixed inset-0 opacity-30 pointer-events-none"
        style={{
          background: `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(139, 92, 246, 0.3), transparent 50%)`
        }}
      />

      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-white/5 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Portfolio
          </h1>
          <div className="flex gap-6">
            <a href="#about" className="text-white/80 hover:text-white transition-colors">About</a>
            <a href="#projects" className="text-white/80 hover:text-white transition-colors">Projects</a>
            <a href="#skills" className="text-white/80 hover:text-white transition-colors">Skills</a>
            <Link href="/showcase" className="text-white/80 hover:text-white transition-colors">Showcase</Link>
            <a href="#contact" className="text-white/80 hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center px-6 pt-20">
        <div 
          className="text-center"
          style={{
            transform: `translateY(${scrollY * 0.5}px)`,
            opacity: 1 - scrollY / 500
          }}
        >
          <div className="mb-8 inline-block">
            <div className="w-32 h-32 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 animate-pulse mx-auto mb-6" />
          </div>
          <h1 className="text-6xl md:text-8xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent animate-gradient">
            Creative Developer
          </h1>
          <p className="text-xl md:text-2xl text-white/70 mb-8 max-w-2xl mx-auto">
            Building beautiful, interactive experiences that make an impact
          </p>
          <div className="flex gap-4 justify-center">
            <a 
              href="#projects"
              className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full text-white font-semibold hover:scale-105 transition-transform"
            >
              View Projects
            </a>
            <a 
              href="#contact"
              className="px-8 py-4 border-2 border-white/30 rounded-full text-white font-semibold hover:bg-white/10 transition-colors"
            >
              Get in Touch
            </a>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-bold text-white mb-12 text-center">About Me</h2>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <p className="text-white/80 text-lg leading-relaxed">
                I'm a passionate developer who loves creating stunning web experiences. 
                With expertise in modern technologies and a keen eye for design, I bring 
                ideas to life through code.
              </p>
              <p className="text-white/80 text-lg leading-relaxed">
                Every project is an opportunity to push boundaries and create something 
                extraordinary that users will love.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-6">
              {[
                { num: "50+", label: "Projects" },
                { num: "5+", label: "Years Exp" },
                { num: "100%", label: "Satisfaction" },
                { num: "24/7", label: "Support" },
              ].map((stat, i) => (
                <div 
                  key={i}
                  className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 text-center hover:bg-white/10 transition-all hover:scale-105"
                >
                  <div className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-2">
                    {stat.num}
                  </div>
                  <div className="text-white/60">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Projects Section */}
      <section id="projects" className="py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-5xl font-bold text-white mb-12 text-center">Featured Projects</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {projects.map((project, i) => (
              <div
                key={i}
                className="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all hover:scale-105 cursor-pointer overflow-hidden"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${project.color} opacity-0 group-hover:opacity-20 transition-opacity`} />
                <div className="relative z-10">
                  <h3 className="text-2xl font-bold text-white mb-3">{project.title}</h3>
                  <p className="text-white/70 mb-6">{project.desc}</p>
                  <div className="flex gap-2">
                    <span className="px-3 py-1 bg-white/10 rounded-full text-sm text-white/80">React</span>
                    <span className="px-3 py-1 bg-white/10 rounded-full text-sm text-white/80">TypeScript</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section id="skills" className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-5xl font-bold text-white mb-12 text-center">Skills & Expertise</h2>
          <div className="space-y-8">
            {skills.map((skill, i) => (
              <div key={i} className="space-y-3">
                <div className="flex justify-between text-white">
                  <span className="font-semibold">{skill.name}</span>
                  <span>{skill.level}%</span>
                </div>
                <div className="h-3 bg-white/10 rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500 rounded-full transition-all duration-1000 ease-out"
                    style={{ width: `${skill.level}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 px-6">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-5xl font-bold text-white mb-12 text-center">Get In Touch</h2>
          <form className="space-y-6">
            <div>
              <input
                type="text"
                placeholder="Your Name"
                className="w-full px-6 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-purple-500 transition-colors"
              />
            </div>
            <div>
              <input
                type="email"
                placeholder="Your Email"
                className="w-full px-6 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-purple-500 transition-colors"
              />
            </div>
            <div>
              <textarea
                rows={6}
                placeholder="Your Message"
                className="w-full px-6 py-4 bg-white/5 border border-white/10 rounded-xl text-white placeholder-white/50 focus:outline-none focus:border-purple-500 transition-colors resize-none"
              />
            </div>
            <button
              type="submit"
              className="w-full px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl text-white font-semibold hover:scale-105 transition-transform"
            >
              Send Message
            </button>
          </form>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-white/10">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-white/60">
            © 2025 Portfolio. Built with Next.js & Tailwind CSS
          </p>
          <div className="flex gap-6 justify-center mt-6">
            <a href="#" className="text-white/60 hover:text-white transition-colors">GitHub</a>
            <a href="#" className="text-white/60 hover:text-white transition-colors">LinkedIn</a>
            <a href="#" className="text-white/60 hover:text-white transition-colors">Twitter</a>
          </div>
        </div>
      </footer>
    </div>
  )
}
