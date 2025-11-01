"use client"

import { useState } from 'react'
import Link from 'next/link'

export default function Showcase() {
  const [activeTab, setActiveTab] = useState('all')

  const showcaseItems = [
    { 
      id: 1, 
      title: "Modern Dashboard", 
      category: "web", 
      gradient: "from-blue-500 to-purple-500",
      description: "Analytics platform with real-time data visualization"
    },
    { 
      id: 2, 
      title: "Mobile App Design", 
      category: "mobile", 
      gradient: "from-pink-500 to-orange-500",
      description: "Fitness tracking app with beautiful UI"
    },
    { 
      id: 3, 
      title: "E-Commerce Store", 
      category: "web", 
      gradient: "from-green-500 to-teal-500",
      description: "Full-featured online shopping experience"
    },
    { 
      id: 4, 
      title: "Brand Identity", 
      category: "design", 
      gradient: "from-purple-500 to-pink-500",
      description: "Complete branding package for tech startup"
    },
    { 
      id: 5, 
      title: "Social Platform", 
      category: "web", 
      gradient: "from-cyan-500 to-blue-500",
      description: "Connect and share with community"
    },
    { 
      id: 6, 
      title: "UI Kit", 
      category: "design", 
      gradient: "from-orange-500 to-red-500",
      description: "Comprehensive component library"
    },
  ]

  const filteredItems = activeTab === 'all' 
    ? showcaseItems 
    : showcaseItems.filter(item => item.category === activeTab)

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 backdrop-blur-md bg-white/5 border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/">
            <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent cursor-pointer">
              Portfolio
            </h1>
          </Link>
          <Link 
            href="/"
            className="text-white/80 hover:text-white transition-colors"
          >
            ← Back to Home
          </Link>
        </div>
      </nav>

      <div className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-16">
            <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-pink-400 to-purple-400 bg-clip-text text-transparent">
              Project Showcase
            </h1>
            <p className="text-xl text-white/70 max-w-2xl mx-auto">
              Explore my latest work across web development, mobile apps, and design
            </p>
          </div>

          {/* Filter Tabs */}
          <div className="flex justify-center gap-4 mb-12 flex-wrap">
            {['all', 'web', 'mobile', 'design'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 rounded-full font-semibold transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white scale-105'
                    : 'bg-white/5 text-white/70 hover:bg-white/10'
                }`}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>

          {/* Showcase Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredItems.map((item, index) => (
              <div
                key={item.id}
                className="group relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden hover:scale-105 transition-all duration-300 cursor-pointer"
                style={{
                  animation: `fadeInUp 0.5s ease-out ${index * 0.1}s both`
                }}
              >
                {/* Image Placeholder with Gradient */}
                <div className={`h-64 bg-gradient-to-br ${item.gradient} relative overflow-hidden`}>
                  <div className="absolute inset-0 bg-black/20 group-hover:bg-black/0 transition-all" />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-32 h-32 border-4 border-white/30 rounded-full group-hover:scale-110 transition-transform" />
                  </div>
                </div>

                {/* Content */}
                <div className="p-6">
                  <div className="flex items-center gap-2 mb-3">
                    <span className="px-3 py-1 bg-white/10 rounded-full text-xs text-white/80 uppercase">
                      {item.category}
                    </span>
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-purple-400 transition-colors">
                    {item.title}
                  </h3>
                  <p className="text-white/70">
                    {item.description}
                  </p>
                </div>

                {/* Hover Overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-purple-500/0 to-pink-500/0 group-hover:from-purple-500/20 group-hover:to-pink-500/20 transition-all pointer-events-none" />
              </div>
            ))}
          </div>

          {/* Call to Action */}
          <div className="mt-20 text-center">
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-3xl p-12 max-w-3xl mx-auto">
              <h2 className="text-4xl font-bold text-white mb-4">
                Like what you see?
              </h2>
              <p className="text-white/70 text-lg mb-8">
                Let's work together to bring your ideas to life
              </p>
              <Link href="/#contact">
                <button className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full text-white font-semibold hover:scale-105 transition-transform">
                  Start a Project
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  )
}
