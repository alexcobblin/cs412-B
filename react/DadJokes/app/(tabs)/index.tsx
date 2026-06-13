// DadJokes/app/(tabs)/index.tsx
import { useState, useEffect, useCallback } from 'react';
import { View, Text, Image, ActivityIndicator, Pressable, ScrollView } from 'react-native';
import { styles } from '../../assets/my-styles';
import { BASE_URL } from '../../assets/config';

type Joke = { text: string; name: string; timestamp: string };
type Picture = { image_url: string; name: string; timestamp: string };

export default function IndexScreen() {
  const [joke, setJoke] = useState<Joke | null>(null);
  const [picture, setPicture] = useState<Picture | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [jokeRes, picRes] = await Promise.all([
        fetch(`${BASE_URL}/api/random`),
        fetch(`${BASE_URL}/api/random_picture`),
      ]);
      const jokeData = await jokeRes.json();
      const picData = await picRes.json();
      console.log('random joke:', jokeData);
      console.log('random picture:', picData);
      setJoke(jokeData);
      setPicture(picData);
    } catch (err) {
      console.error('Error loading random content:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.titleText}>Dad Joke of the Moment</Text>

      {joke && (
        <View style={styles.card}>
          <Text style={styles.jokeText}>{joke.text}</Text>
          <Text style={styles.contributor}>by {joke.name}</Text>
        </View>
      )}

      {picture && (
        <Image source={{ uri: picture.image_url }} style={styles.image} resizeMode="contain" />
      )}

      <Pressable style={styles.button} onPress={load}>
        <Text style={styles.buttonText}>Show me another</Text>
      </Pressable>
    </ScrollView>
  );
}