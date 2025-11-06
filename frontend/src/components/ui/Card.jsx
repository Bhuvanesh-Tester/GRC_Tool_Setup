export default function Card({ children, className = '' }) {
  return (
    <div className={`bg-white shadow rounded p-4 ${className}`}>{children}</div>
  )
}