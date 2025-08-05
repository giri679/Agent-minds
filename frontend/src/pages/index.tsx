import { useState, useEffect } from 'react';
import Head from 'next/head';
import StudentDashboard from '../components/StudentDashboard';
import TeacherDashboard from '../components/TeacherDashboard';
import AIFeatures from '../components/AIFeatures';

export default function Home() {
  const [currentTab, setCurrentTab] = useState(0);
  const [apiStatus, setApiStatus] = useState<'loading' | 'connected' | 'error'>('loading');
  const [systemInfo, setSystemInfo] = useState<any>(null);

  useEffect(() => {
    checkApiConnection();
  }, []);

  const checkApiConnection = async () => {
    try {
      const response = await fetch('/api/health');
      const data = await response.json();
      setSystemInfo(data);
      setApiStatus('connected');
    } catch (error) {
      console.error('API connection failed:', error);
      setApiStatus('error');
    }
  };

  return (
    <>
      <Head>
        <title>🤖 AI Education Agent - Government Schools</title>
        <meta name="description" content="AI-powered personalized learning system for government schools" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center space-x-3">
                <div className="text-3xl">🤖</div>
                <div>
                  <h1 className="text-2xl font-bold">AI Education Agent</h1>
                  <p className="text-blue-100 text-sm">Government Schools - Personalized Learning</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                  apiStatus === 'connected' ? 'bg-green-500 text-white' :
                  apiStatus === 'loading' ? 'bg-yellow-500 text-white' :
                  'bg-red-500 text-white'
                }`}>
                  {apiStatus === 'connected' ? '✅ AI Connected' :
                   apiStatus === 'loading' ? '⏳ Connecting...' :
                   '❌ Offline'}
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* System Info Banner */}
        {systemInfo && (
          <div className="bg-blue-500 text-white text-center py-2">
            <p className="text-sm">
              🎓 {systemInfo.message} | Version {systemInfo.version} |
              OpenAI Status: {systemInfo.openai_status === 'connected' ? '✅ Connected' : '❌ Not Connected'}
            </p>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="bg-white shadow">
          <div className="max-w-7xl mx-auto">
            <nav className="flex space-x-8" aria-label="Tabs">
              <button
                onClick={() => setCurrentTab(0)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  currentTab === 0
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span>📚</span>
                  <span>Student Dashboard</span>
                </div>
              </button>
              <button
                onClick={() => setCurrentTab(1)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  currentTab === 1
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span>👨‍🏫</span>
                  <span>Teacher Dashboard</span>
                </div>
              </button>
              <button
                onClick={() => setCurrentTab(2)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  currentTab === 2
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span>🤖</span>
                  <span>AI Features</span>
                </div>
              </button>
            </nav>
          </div>
        </div>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            {currentTab === 0 && <StudentDashboard apiStatus={apiStatus} />}
            {currentTab === 1 && <TeacherDashboard apiStatus={apiStatus} />}
            {currentTab === 2 && <AIFeatures apiStatus={apiStatus} />}
          </div>
        </main>

        {/* Floating AI Button */}
        <button
          onClick={() => setCurrentTab(2)}
          className="fixed bottom-6 right-6 bg-gradient-to-r from-purple-500 to-purple-600 text-white p-4 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          title="AI Features"
        >
          <span className="text-2xl">🤖</span>
        </button>
      </div>
    </>
  );
}