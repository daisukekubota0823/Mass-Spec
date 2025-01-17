import { useState } from "react";
import { Link } from "react-router-dom";
import { FiMail, FiArrowRight, FiCheck } from "react-icons/fi";
// import Logo from "../components/Logo";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle password reset logic here
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-cyan-50 via-white to-blue-50">
      <div className="absolute top-4 left-4">
        <Link to="/">{/* <Logo /> */}</Link>
      </div>

      <div className="flex items-center justify-center min-h-screen px-4">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-2xl shadow-xl p-8 space-y-6">
            {!submitted ? (
              <>
                <div className="text-center space-y-2">
                  <h1 className="text-3xl font-bold text-gray-900">
                    Reset Password
                  </h1>
                  <p className="text-gray-500">
                    Enter your email to receive reset instructions
                  </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email Address
                    </label>
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <FiMail className="h-5 w-5 text-gray-400" />
                      </div>
                      <input
                        type="email"
                        required
                        className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent"
                        placeholder="Enter your email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                      />
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-base font-medium rounded-lg text-white bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500"
                  >
                    Send Reset Link
                    <FiArrowRight className="ml-2" />
                  </button>
                </form>
              </>
            ) : (
              <div className="text-center space-y-6">
                <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-full bg-green-100">
                  <FiCheck className="h-6 w-6 text-green-500" />
                </div>
                <div className="space-y-2">
                  <h2 className="text-2xl font-bold text-gray-900">
                    Check your email
                  </h2>
                  <p className="text-gray-500">
                    We've sent a password reset link to
                    <br />
                    <span className="font-medium text-gray-700">{email}</span>
                  </p>
                </div>
                <div className="space-y-4">
                  <p className="text-sm text-gray-500">
                    Didn't receive the email? Check your spam folder or
                  </p>
                  <button
                    onClick={() => setSubmitted(false)}
                    className="text-sm font-medium text-cyan-600 hover:text-cyan-500"
                  >
                    Try another email address
                  </button>
                </div>
              </div>
            )}

            <div className="text-center">
              <p className="text-sm text-gray-600">
                Remember your password?{" "}
                <Link
                  to="/login"
                  className="font-medium text-cyan-600 hover:text-cyan-500"
                >
                  Back to login
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
