import React, { useState } from 'react';
import { View, Text, TextInput, Button, ScrollView, StyleSheet, ActivityIndicator, useColorScheme } from 'react-native';
import axios from 'axios';

const AIChatScreen = () => {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [debugInfo, setDebugInfo] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';

  const handleSubmit = async () => {
    if (!input.trim()) return;

    setLoading(true);
    try {
      const res = await fetch('http://192.168.8.7:8000/user-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setResponse(data.response);
      setDebugInfo(data);
    } catch (err) {
      console.error('❌ Error:', err);
      setResponse('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={[
      styles.container,
      { backgroundColor: isDark ? '#181a20' : '#fff' }
    ]}>
      <Text style={[
        styles.heading,
        { color: isDark ? '#fff' : '#000' }
      ]}>🤖 AI Food Assistant</Text>

      <TextInput
        style={[
          styles.input,
          {
            backgroundColor: isDark ? '#23262f' : '#fff',
            color: isDark ? '#fff' : '#000',
            borderColor: isDark ? '#444' : '#aaa',
          }
        ]}
        placeholder="Ask something like 'Find spicy vegetarian food under 300₹'"
        placeholderTextColor={isDark ? '#aaa' : '#888'}
        multiline
        value={input}
        onChangeText={setInput}
      />

      <Button title={loading ? 'Thinking...' : 'Send'} onPress={handleSubmit} disabled={loading} />

      {loading && <ActivityIndicator size="large" color="#ff6600" style={{ marginTop: 16 }} />}

      {response && (
        <View style={[
          styles.responseBox,
          { backgroundColor: isDark ? '#23262f' : '#f4f4f4' }
        ]}>
          <Text style={[
            styles.label,
            { color: isDark ? '#fff' : '#000' }
          ]}>AI Response:</Text>
          <Text style={{ color: isDark ? '#fff' : '#000' }}>{response}</Text>
        </View>
      )}

      {debugInfo && false && ( 
        <View style={[
          styles.debugBox,
          { backgroundColor: isDark ? '#1a1d23' : '#eef7ff' }
        ]}>
          <Text style={[
            styles.label,
            { color: isDark ? '#fff' : '#000' }
          ]}>Debug Info (for devs):</Text>
          <Text selectable style={{ color: isDark ? '#fff' : '#000' }}>
            {JSON.stringify(debugInfo, null, 2)}
          </Text>
        </View>
      )}
    </ScrollView>
  );
};

export default AIChatScreen;

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  heading: {
    fontSize: 22,
    fontWeight: '600',
    marginBottom: 20,
  },
  input: {
    borderColor: '#aaa',
    borderWidth: 1,
    padding: 12,
    borderRadius: 10,
    minHeight: 80,
    marginBottom: 10,
    textAlignVertical: 'top',
  },
  responseBox: {
    marginTop: 20,
    backgroundColor: '#f4f4f4',
    padding: 16,
    borderRadius: 10,
  },
  debugBox: {
    marginTop: 20,
    backgroundColor: '#eef7ff',
    padding: 16,
    borderRadius: 10,
  },
  label: {
    fontWeight: 'bold',
    marginBottom: 8,
  },
});