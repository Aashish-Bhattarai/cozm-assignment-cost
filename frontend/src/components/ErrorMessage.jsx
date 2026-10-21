// One or more error messages from the API, rendered as a list.

export default function ErrorMessage({ messages }) {
  if (!messages || messages.length === 0) {
    return null;
  }
  return (
    <ul className="error-messages">
      {messages.map((message) => (
        <li key={message}>{message}</li>
      ))}
    </ul>
  );
}
