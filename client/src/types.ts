export interface UserPublic {
  id: number;
  username: string;
  kem_public_key: string;
  sign_public_key: string;
  created_at: string;
}

export interface MessageRecord {
  id: number;
  sender_id: number;
  recipient_id: number;
  kem_ciphertext: string;
  ciphertext: string;
  nonce: string;
  signature: string;
  created_at: string;
}

export interface KeyBundle {
  username: string;
  kem_public_key: string;
  kem_private_key: string;
  sign_public_key: string;
  sign_private_key: string;
  created_at: string;
}

