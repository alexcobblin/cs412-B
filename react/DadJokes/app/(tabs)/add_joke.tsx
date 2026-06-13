// DadJokes/app/(tabs)/add_joke.tsx
import { useState } from 'react';
import { Text, TextInput, Pressable, ScrollView, Alert } from 'react-native';
import { styles } from '../../assets/my_styles';
import { BASE_URL } from '../../assets/config';

export default function AddJokeScreen() {
  const [text, setText] = useState('');
  const [name, setName] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const submit = async () => {
    if (!text.trim() || !name.trim()) {
      Alert.alert('Missing info', 'Please enter both a joke and your name.');
      return;
    }

    setSubmitting(true);
    const payload = { text, name };
    console.log('POSTing joke:', payload);

    try {
      const res = await fetch(`${BASE_URL}/api/jokes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      console.log('POST status:', res.status);

      if (res.ok) {
        Alert.alert('Success', 'Your joke was added!');
        setText('');
        setName('');
      } else {
        const errText = await res.text();
        console.error('POST failed:', errText);
        Alert.alert('Error', 'Could not add joke. Status ' + res.status);
      }
    } catch (err) {
      console.error('Network error:', err);
      Alert.alert('Error', 'Network problem. Double check your BASE_URL.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.titleText}>Add a New Joke</Text>

      <Text style={styles.label}>Joke</Text>
      <TextInput
        style={styles.input}
        value={text}
        onChangeText={setText}
        placeholder="Why did the..."
        multiline
      />

      <Text style={styles.label}>Your name</Text>
      <TextInput
        style={styles.input}
        value={name}
        onChangeText={setName}
        placeholder="Contributor name"
      />

      <Pressable style={styles.button} onPress={submit} disabled={submitting}>
        <Text style={styles.buttonText}>{submitting ? 'Submitting...' : 'Submit Joke'}</Text>
      </Pressable>
    </ScrollView>
  );
}