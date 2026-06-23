// DadJokes/app/(tabs)/jokes_list.tsx
import { useState, useEffect } from 'react';
import { View, Text, FlatList, ActivityIndicator } from 'react-native';
import { styles } from '../../assets/my-styles';
import { BASE_URL } from '../../assets/config';

type Joke = { id?: number; text: string; name: string; timestamp: string };

export default function JokeListScreen() {
  const [jokes, setJokes] = useState<Joke[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${BASE_URL}/api/jokes`);
        const data = await res.json();
        console.log('fetched jokes count:', data.length);
        setJokes(data);
      } catch (err) {
        console.error('Error loading jokes:', err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <FlatList
      contentContainerStyle={styles.container}
      data={jokes}
      keyExtractor={(item, index) => String(item.id ?? index)}
      ListHeaderComponent={<Text style={styles.titleText}>All Jokes</Text>}
      renderItem={({ item }) => (
        <View style={styles.card}>
          <Text style={styles.jokeText}>{item.text}</Text>
          <Text style={styles.contributor}>by {item.name}</Text>
        </View>
      )}
    />
  );
}