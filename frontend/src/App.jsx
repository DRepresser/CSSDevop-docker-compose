import { useEffect, useState } from 'react'
import './index.css'

function StarRating({ rating }) {
  const stars = Math.round(rating || 0)
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map(i => (
        <span key={i} className={i <= stars ? 'text-yellow-400' : 'text-gray-300'}>★</span>
      ))}
      <span className="text-xs text-gray-500 ml-1">{rating ? rating.toFixed(1) : 'N/A'}</span>
    </div>
  )
}

function App() {
  const [resumes, setResumes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Fetch ผ่าน /api ซึ่ง Caddy จะ Route ไปหา Backend ให้
    fetch('/api/resumes/')
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        return res.json()
      })
      .then(data => {
        setResumes(Array.isArray(data) ? data : (data.results || []))
        setLoading(false)
      })
      .catch(err => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-blue-600 text-white py-6 shadow-lg">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold text-center">Resume Hub</h1>
          <p className="text-center text-blue-200 mt-1">Browse professional resumes</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto p-6">
        {loading && (
          <div className="text-center py-20">
            <div className="text-gray-500 text-xl">Loading resumes...</div>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            <strong>Error:</strong> {error}
          </div>
        )}

        {!loading && !error && resumes.length === 0 && (
          <div className="text-center py-20 text-gray-500">
            <p className="text-xl">No resumes found.</p>
            <p className="text-sm mt-2">Run <code className="bg-gray-200 px-1 rounded">generate_resumes</code> to seed data.</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resumes.map(resume => (
            <div key={resume.id} className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300">
              {/* Avatar + Name */}
              <div className="flex items-center gap-3 mb-4">
                {resume.profile_image ? (
                  <img src={resume.profile_image} alt="profile" className="w-12 h-12 rounded-full object-cover" />
                ) : (
                  <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold text-lg">
                    {(resume.owner_full_name || resume.owner_username || '?')[0].toUpperCase()}
                  </div>
                )}
                <div>
                  <h2 className="text-lg font-bold text-gray-800">{resume.owner_full_name || resume.owner_username}</h2>
                  <p className="text-xs text-gray-500">@{resume.owner_username}</p>
                </div>
              </div>

              {/* Summary */}
              <p className="text-gray-600 text-sm mb-4 line-clamp-3">{resume.success_summary}</p>

              {/* Rating */}
              <StarRating rating={resume.avg_rating} />

              {/* Skills */}
              {resume.skills && resume.skills.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {resume.skills.slice(0, 5).map(skill => (
                    <span key={skill.id} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                      {skill.name}
                    </span>
                  ))}
                  {resume.skills.length > 5 && (
                    <span className="text-xs text-gray-400">+{resume.skills.length - 5} more</span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}

export default App
