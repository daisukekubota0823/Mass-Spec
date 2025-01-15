import {
  FiDatabase,
  FiSearch,
  FiBarChart2,
  FiArrowRight,
  FiZap,
  FiAward,
  FiTrendingUp,
  FiUsers,
} from "react-icons/fi";
import { Link } from "react-router-dom";
import logo from "../../assets/logo.png";

export default function Homepage() {
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
      {/* Hero Section with animated gradient */}
      <div className="relative overflow-hidden py-20 px-6">
        <div className="absolute inset-0 bg-gradient-to-r from-violet-100 via-cyan-100 to-emerald-100 opacity-50"></div>
        <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
        <div className="relative max-w-7xl mx-auto text-center">
          <div className="animate-fade-in">
            <img src={logo} alt="Logo" className="mx-auto mb-6 w-32" />
            <h1 className="text-6xl font-bold text-gray-900 mb-6 bg-clip-text text-transparent bg-gradient-to-r from-violet-600 to-cyan-600">
              LAmass
            </h1>
            <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              Experience the next generation of mass spectrometry analysis with
              our comprehensive suite of tools. Faster, more accurate, and more
              intuitive than ever before.
            </p>
            <div className="flex justify-center gap-6">
              <button className="px-8 py-4 bg-gradient-to-r from-violet-600 to-cyan-600 text-white rounded-xl font-semibold hover:from-violet-700 hover:to-cyan-700 transition-all transform hover:scale-105 shadow-lg">
                Get Started
              </button>
              <button className="px-8 py-4 bg-white text-gray-800 rounded-xl font-semibold border-2 border-gray-200 hover:border-violet-600 transition-all transform hover:scale-105 shadow-lg">
                Watch Demo
              </button>
            </div>
          </div>
        </div>
      </div>

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

      {/* Tools Section with gradient cards */}
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
                  <div className="flex items-center text-violet-600 font-semibold group-hover:translate-x-2 transition-transform">
                    Explore Tool
                    <FiArrowRight className="ml-2" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="py-16 px-6 bg-gradient-to-br from-gray-50 to-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-16">
            Advanced Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                name: "Automated Processing",
                color: "from-blue-500 to-cyan-400",
              },
              {
                name: "Interactive Visualizations",
                color: "from-purple-500 to-pink-400",
              },
              {
                name: "Formula Prediction",
                color: "from-emerald-500 to-teal-400",
              },
              {
                name: "Structure Elucidation",
                color: "from-orange-500 to-red-400",
              },
              {
                name: "Peak Detection",
                color: "from-violet-500 to-purple-400",
              },
              { name: "MS/MS Analysis", color: "from-teal-500 to-green-400" },
              { name: "MRM Optimization", color: "from-pink-500 to-rose-400" },
              { name: "Data Export", color: "from-cyan-500 to-blue-400" },
            ].map((feature) => (
              <div
                key={feature.name}
                className="bg-white rounded-2xl shadow-lg p-6 transform hover:scale-105 transition-all duration-300 hover:shadow-xl"
              >
                <div
                  className={`h-2 w-20 rounded-full bg-gradient-to-r ${feature.color} mb-4`}
                ></div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {feature.name}
                </h3>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="py-20 px-6 bg-gradient-to-br from-violet-50 to-cyan-50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Ready to Transform Your Research?
          </h2>
          <p className="text-xl text-gray-600 mb-8 leading-relaxed">
            Join thousands of researchers worldwide who are accelerating their
            discoveries with MS-Dial Workbench
          </p>
          <button className="px-8 py-4 bg-gradient-to-r from-violet-600 to-cyan-600 text-white rounded-xl font-semibold hover:from-violet-700 hover:to-cyan-700 transition-all transform hover:scale-105 shadow-lg">
            Start Your Journey
          </button>
        </div>
      </div>
    </div>
  );
}
