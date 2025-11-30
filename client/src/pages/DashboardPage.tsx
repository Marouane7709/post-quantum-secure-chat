import { FormEvent, useEffect, useState } from "react";
import api from "../api";
import { useAuth } from "../contexts/AuthContext";
import { MessageRecord, UserPublic } from "../types";

export function DashboardPage() {
  const { token } = useAuth();
  const [recipient, setRecipient] = useState("");
  const [message, setMessage] = useState("");
  const [users, setUsers] = useState<UserPublic[]>([]);
  const [inbox, setInbox] = useState<MessageRecord[]>([]);
  const [decryptions, setDecryptions] = useState<Record<number, string>>({});
  const [sending, setSending] = useState(false);
  const [status, setStatus] = useState("");

  const authHeaders = token ? { Authorization: `Bearer ${token}` } : {};

  const fetchUsers = async () => {
    try {
      const { data } = await api.get<UserPublic[]>("/users");
      setUsers(data);
      if (!recipient && data.length > 0) {
        setRecipient(data[0].username);
      }
    } catch (err) {
      console.error("Failed to fetch users", err);
    }
  };

  const fetchInbox = async () => {
    if (!token) return;
    try {
      const { data } = await api.get<MessageRecord[]>("/messages/inbox", { headers: authHeaders });
      setInbox(data);
    } catch (err) {
      console.error("Failed to fetch inbox", err);
    }
  };

  const handleSend = async (evt: FormEvent) => {
    evt.preventDefault();
    if (!token) {
      setStatus("Please login first.");
      return;
    }
    setSending(true);
    setStatus("Sending message...");
    try {
      await api.post(
        "/messages",
        { recipient_username: recipient, plaintext: message },
        { headers: authHeaders }
      );
      setMessage("");
      setStatus("Message encrypted and delivered.");
      fetchInbox();
    } catch (err: any) {
      setStatus(err.response?.data?.detail || "Failed to send message.");
    } finally {
      setSending(false);
    }
  };

  const decryptMessage = async (messageId: number) => {
    if (!token) return;
    try {
      const { data } = await api.post<{ plaintext: string }>(
        `/messages/${messageId}/decrypt`,
        {},
        { headers: authHeaders }
      );
      setDecryptions((prev) => ({ ...prev, [messageId]: data.plaintext }));
      setStatus(`Message ${messageId} decrypted.`);
    } catch (err: any) {
      setStatus(err.response?.data?.detail || "Decryption failed.");
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  useEffect(() => {
    if (token) {
      fetchInbox();
      const interval = setInterval(fetchInbox, 5000);
      return () => clearInterval(interval);
    }
  }, [token]);

  return (
    <div className="dashboard">
      {status && <div className="dashboard-status">{status}</div>}

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h2>Send Quantum-Hardened Message</h2>
          <form onSubmit={handleSend}>
            <div className="form-group">
              <label htmlFor="recipient">Recipient</label>
              <select
                id="recipient"
                value={recipient}
                onChange={(e) => setRecipient(e.target.value)}
                required
                disabled={sending}
              >
                {users.map((user) => (
                  <option key={user.id} value={user.username}>
                    {user.username}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="message">Message</label>
              <textarea
                id="message"
                rows={4}
                placeholder="Message contents"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                required
                disabled={sending}
              />
            </div>

            <button type="submit" className="dashboard-button" disabled={sending || !token}>
              {sending ? "Sending..." : "Encrypt & Send"}
            </button>

            <p className="dashboard-caption">
              Server encapsulates via Kyber, encrypts with AES-GCM, signs with Dilithium2.
            </p>
          </form>
        </div>

        <div className="dashboard-card">
          <h2>Inbox ({inbox.length})</h2>
          {inbox.length === 0 ? (
            <div className="inbox-empty">
              <p>No messages yet. Send a quantum-hardened message to see it here.</p>
            </div>
          ) : (
            <div className="inbox-list">
              {inbox.map((item) => (
                <div key={item.id} className="inbox-item">
                  <div className="inbox-item-header">
                    <span className="inbox-item-id">Envelope #{item.id}</span>
                    <span className="inbox-item-time">
                      {new Date(item.created_at).toLocaleString()}
                    </span>
                  </div>
                  <p className="inbox-item-preview">
                    <strong>KEM CT:</strong> {item.kem_ciphertext.slice(0, 40)}...
                  </p>
                  {decryptions[item.id] ? (
                    <div className="inbox-item-decrypted">
                      <strong>Plaintext:</strong> {decryptions[item.id]}
                    </div>
                  ) : (
                    <button
                      className="inbox-decrypt-btn"
                      onClick={() => decryptMessage(item.id)}
                    >
                      Decrypt with Stored Keys
                    </button>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

