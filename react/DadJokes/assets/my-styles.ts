// DadJokes/assets/my_styles.ts
import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  container: {
    padding: 20,
    gap: 16,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  titleText: {
    fontSize: 24,
    fontWeight: '700',
    marginBottom: 8,
  },
  card: {
    backgroundColor: '#f4f4f5',
    borderRadius: 12,
    padding: 16,
  },
  jokeText: {
    fontSize: 18,
    lineHeight: 26,
  },
  contributor: {
    marginTop: 8,
    fontStyle: 'italic',
    color: '#666',
  },
  image: {
    width: '100%',
    height: 250,
    borderRadius: 12,
  },
  button: {
    backgroundColor: '#2563eb',
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 10,
    padding: 12,
    fontSize: 16,
    minHeight: 48,
  },
});