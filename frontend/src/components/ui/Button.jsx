export default function Button({ children, className = '', ...props }) {
  return (
    <button
      className={`px-3 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-400 ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}