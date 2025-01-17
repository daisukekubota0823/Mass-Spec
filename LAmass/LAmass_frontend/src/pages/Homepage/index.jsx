import {
  FiDatabase,
  FiSearch,
  FiBarChart2,
  FiArrowRight,
  FiZap,
  FiAward,
  FiTrendingUp,
  FiUsers,
  FiMail,
  FiPhone,
  FiMapPin,
  FiGlobe,
  FiLinkedin,
  FiTwitter,
  FiGithub,
} from "react-icons/fi";
import { Link } from "react-router-dom";
import Logo from "../../assets/logo.png";

export default function Dashboard() {
  const tools = [
    {
      name: "MS-DIAL",
      description:
        "Data-independent MS/MS deconvolution for untargeted metabolomics",
      icon: FiDatabase,
      path: "/ms-dial",
      features: [
        "Automated peak detection",
        "MS2 spectrum deconvolution",
        "Alignment of peak spots",
      ],
      color: "from-blue-500 to-cyan-400",
    },
    {
      name: "MS-FINDER",
      description: "Structure elucidation of unknown metabolites",
      icon: FiSearch,
      path: "/ms-finder",
      features: [
        "Formula prediction",
        "Structure prediction",
        "MS/MS fragment annotation",
      ],
      color: "from-purple-500 to-pink-400",
    },
    {
      name: "MRMprobs",
      description: "Automated optimization of MRM transitions",
      icon: FiBarChart2,
      path: "/mrm-probs",
      features: [
        "MRM transition optimization",
        "Retention time prediction",
        "Collision energy optimization",
      ],
      color: "from-emerald-500 to-teal-400",
    },
  ];

  const stats = [
    {
      name: "Active Users",
      value: "10K+",
      icon: FiUsers,
      color: "bg-blue-100 text-blue-600",
    },
    {
      name: "Analysis Run",
      value: "1M+",
      icon: FiZap,
      color: "bg-purple-100 text-purple-600",
    },
    {
      name: "Success Rate",
      value: "99.9%",
      icon: FiAward,
      color: "bg-emerald-100 text-emerald-600",
    },
    {
      name: "Processing Speed",
      value: "2x Faster",
      icon: FiTrendingUp,
      color: "bg-orange-100 text-orange-600",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-white">
      {/* Logo Section with enhanced styling */}
      <div className="absolute top-8 left-8 z-50 transform hover:scale-105 transition-transform">
        <div className="bg-white/80 backdrop-blur-sm p-4 rounded-xl shadow-lg">
          {/* <Logo /> */}
        </div>
      </div>

      {/* Hero Section with animated gradient */}
      <div className="relative overflow-hidden py-20 px-6">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-100 via-blue-100 to-purple-100 opacity-50"></div>
        <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
        <div className="relative max-w-7xl mx-auto text-center pt-16">
          <div className="animate-fade-in">
            <h1 className="text-6xl font-bold text-gray-900 mb-6 bg-clip-text text-transparent bg-gradient-to-r from-cyan-600 to-blue-600">
              LAmass Web Workbench
            </h1>
            <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              Experience the next generation of mass spectrometry analysis with
              our comprehensive suite of tools. Faster, more accurate, and more
              intuitive than ever before.
            </p>
            <div className="flex justify-center gap-6">
              <button className="px-8 py-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-xl font-semibold hover:from-cyan-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-lg">
                Get Started
              </button>
              <button className="px-8 py-4 bg-white text-gray-800 rounded-xl font-semibold border-2 border-gray-200 hover:border-cyan-600 transition-all transform hover:scale-105 shadow-lg">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Rest of the Dashboard component remains the same */}
      {/* Stats Section */}
      <div className="py-16 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat) => (
              <div
                key={stat.name}
                className="bg-white rounded-2xl shadow-xl p-6 transform hover:scale-105 transition-all"
              >
                <div
                  className={`inline-block p-3 rounded-lg ${stat.color} mb-4`}
                >
                  <stat.icon className="w-6 h-6" />
                </div>
                <h3 className="text-3xl font-bold text-gray-900">
                  {stat.value}
                </h3>
                <p className="text-gray-600 mt-1">{stat.name}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tools Section */}
      <div className="py-16 px-6">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-16">
            Powerful Tools for Mass Spectrometry Analysis
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {tools.map((tool) => (
              <Link
                key={tool.name}
                to={tool.path}
                className="group relative bg-white rounded-2xl shadow-xl overflow-hidden transform hover:scale-105 transition-all duration-300"
              >
                <div
                  className={`absolute inset-0 bg-gradient-to-br ${tool.color} opacity-0 group-hover:opacity-10 transition-opacity`}
                ></div>
                <div className="p-8">
                  <div className="mb-6">
                    <tool.icon className="w-12 h-12 text-gray-900" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">
                    {tool.name}
                  </h3>
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    {tool.description}
                  </p>
                  <div className="space-y-3 mb-6">
                    {tool.features.map((feature) => (
                      <div
                        key={feature}
                        className="flex items-center text-gray-600"
                      >
                        <FiArrowRight className="w-4 h-4 mr-2 text-gray-400" />
                        {feature}
                      </div>
                    ))}
                  </div>
                  <div className="flex items-center text-cyan-600 font-semibold group-hover:translate-x-2 transition-transform">
                    Explore Tool
                    <FiArrowRight className="ml-2" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Call to Action */}
      <div className="py-20 px-6 bg-gradient-to-br from-cyan-50 to-blue-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Ready to Transform Your Research?
          </h2>
          <p className="text-xl text-gray-600 mb-8 leading-relaxed">
            Join thousands of researchers worldwide who are accelerating their
            discoveries with LAmass web Workbench
          </p>
          <button className="px-8 py-4 bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-xl font-semibold hover:from-cyan-700 hover:to-blue-700 transition-all transform hover:scale-105 shadow-lg">
            Start Your Journey
          </button>
        </div>
      </div>
      {/* Footer Section */}
      <footer className="bg-gray-900 text-white pt-20 pb-10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
            {/* Company Info */}
            <div className="space-y-6">
              <div className="flex items-center">{/* <Logo /> */}</div>
              <p className="text-gray-400 leading-relaxed">
                Advancing mass spectrometry analysis through innovative
                solutions and cutting-edge technology.
              </p>
              <div className="flex space-x-4">
                <a
                  href="#"
                  className="text-gray-400 hover:text-cyan-500 transition-colors"
                >
                  <FiLinkedin className="w-6 h-6" />
                </a>
                <a
                  href="#"
                  className="text-gray-400 hover:text-cyan-500 transition-colors"
                >
                  <FiTwitter className="w-6 h-6" />
                </a>
                <a
                  href="#"
                  className="text-gray-400 hover:text-cyan-500 transition-colors"
                >
                  <FiGithub className="w-6 h-6" />
                </a>
              </div>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="text-lg font-semibold mb-6">Quick Links</h3>
              <ul className="space-y-4">
                <li>
                  <Link
                    to="/about"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    About Us
                  </Link>
                </li>
                <li>
                  <Link
                    to="/services"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Services
                  </Link>
                </li>
                <li>
                  <Link
                    to="/research"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Research
                  </Link>
                </li>
                <li>
                  <Link
                    to="/publications"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Publications
                  </Link>
                </li>
                <li>
                  <Link
                    to="/blog"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Blog
                  </Link>
                </li>
              </ul>
            </div>

            {/* Contact Info */}
            <div>
              <h3 className="text-lg font-semibold mb-6">Contact Us</h3>
              <ul className="space-y-4">
                <li className="flex items-center text-gray-400">
                  <FiMapPin className="w-5 h-5 mr-3 text-cyan-500" />
                  <span>123 Science Park, Innovation Valley, CA 94025</span>
                </li>
                <li className="flex items-center text-gray-400">
                  <FiPhone className="w-5 h-5 mr-3 text-cyan-500" />
                  <span>+1 (555) 123-4567</span>
                </li>
                <li className="flex items-center text-gray-400">
                  <FiMail className="w-5 h-5 mr-3 text-cyan-500" />
                  <span>contact@lanalytics.com</span>
                </li>
                <li className="flex items-center text-gray-400">
                  <FiGlobe className="w-5 h-5 mr-3 text-cyan-500" />
                  <span>www.lanalytics.com</span>
                </li>
              </ul>
            </div>

            {/* Career & Support */}
            <div>
              <h3 className="text-lg font-semibold mb-6">Career & Support</h3>
              <ul className="space-y-4">
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Career Opportunities
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Technical Support
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Documentation
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Training Programs
                  </a>
                </li>
                <li>
                  <a
                    href="#"
                    className="text-gray-400 hover:text-cyan-500 transition-colors"
                  >
                    Community Forum
                  </a>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom Footer */}
          <div className="pt-8 border-t border-gray-800">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="text-gray-400 text-sm">
                © 2024 LAnalytics. All rights reserved.
              </div>
              <div className="flex space-x-6 text-sm text-gray-400 md:justify-end">
                <a href="#" className="hover:text-cyan-500 transition-colors">
                  Privacy Policy
                </a>
                <a href="#" className="hover:text-cyan-500 transition-colors">
                  Terms of Service
                </a>
                <a href="#" className="hover:text-cyan-500 transition-colors">
                  Cookie Policy
                </a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
