export default function LoadingScreen({ message, subtle = false }) {
  return (
    <div className={subtle ? "loading-banner" : "loading-screen"}>
      <div className="spinner" />
      <p>{message}</p>
    </div>
  );
}
