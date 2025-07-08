import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, ActivityIndicator, useColorScheme } from 'react-native';

interface Restaurant {
  name: string;
  veg: boolean;
  spice_level: string;
  price: number;
}

interface Order {
  dish: string;
  quantity: number;
}

interface APIResponse {
  action: string;
  params: any;
  result: Restaurant[] | Order | Order[];
  response: string;
}

const AIChatScreen = () => {
  const [input, setInput] = useState('');
  const [responses, setResponses] = useState<APIResponse[]>([]);
  const [loading, setLoading] = useState(false);

  const clearConversation = () => {
    setResponses([]);
  };

  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';

  const handleSubmit = async () => {
    if (!input.trim()) return;

    setLoading(true);
    try {
      const res = await fetch('http://100.72.217.76:8000/user-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data: APIResponse = await res.json();
      setResponses(prev => [...prev, data]);
      setInput(''); // Clear input after successful response
    } catch (err) {
      console.error('❌ Error:', err);
      // Add error response to chat
      setResponses(prev => [...prev, {
        action: 'error',
        params: {},
        result: [],
        response: 'Something went wrong. Please try again.'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const renderRestaurantCard = (restaurant: Restaurant, index: number) => (
    <View key={index} style={[
      styles.restaurantCard,
      { backgroundColor: isDark ? '#2a2d36' : '#f8f9fa' }
    ]}>
      <Text style={[styles.restaurantName, { color: isDark ? '#fff' : '#000' }]}>
        {restaurant.name}
      </Text>
      <View style={styles.restaurantDetails}>
        <Text style={[styles.detailText, { color: isDark ? '#aaa' : '#666' }]}>
          {restaurant.veg ? '🌱 Vegetarian' : '🍖 Non-Vegetarian'}
        </Text>
        <Text style={[styles.detailText, { color: isDark ? '#aaa' : '#666' }]}>
          🌶️ {restaurant.spice_level}
        </Text>
        <Text style={[styles.priceText, { color: isDark ? '#4ade80' : '#059669' }]}>
          ₹{restaurant.price}
        </Text>
      </View>
    </View>
  );

  const renderOrderCard = (order: Order, index: number) => (
    <View key={index} style={[
      styles.orderCard,
      { backgroundColor: isDark ? '#2a2d36' : '#f8f9fa' }
    ]}>
      <Text style={[styles.orderDish, { color: isDark ? '#fff' : '#000' }]}>
        {order.dish}
      </Text>
      <Text style={[styles.orderQuantity, { color: isDark ? '#aaa' : '#666' }]}>
        Qty: {order.quantity}
      </Text>
    </View>
  );

  const renderResponse = (response: APIResponse, index: number) => (
    <View key={index} style={[
      styles.responseContainer,
      { backgroundColor: isDark ? '#23262f' : '#f4f4f4' }
    ]}>
      <Text style={[styles.responseText, { color: isDark ? '#fff' : '#000' }]}>
        {response.response}
      </Text>
      
      {response.action === 'find_restaurant' && Array.isArray(response.result) && (
        <View style={styles.resultsContainer}>
          <Text style={[styles.sectionTitle, { color: isDark ? '#4ade80' : '#059669' }]}>
            🍽️ Available Restaurants
          </Text>
          {(response.result as Restaurant[]).map((restaurant, idx) => 
            renderRestaurantCard(restaurant, idx)
          )}
        </View>
      )}
      
      {response.action === 'food_order' && !Array.isArray(response.result) && (
        <View style={styles.resultsContainer}>
          <Text style={[styles.sectionTitle, { color: isDark ? '#4ade80' : '#059669' }]}>
            ✅ Order Confirmed
          </Text>
          {renderOrderCard(response.result as Order, 0)}
        </View>
      )}
      
      {response.action === 'get_past_orders' && Array.isArray(response.result) && (
        <View style={styles.resultsContainer}>
          <Text style={[styles.sectionTitle, { color: isDark ? '#4ade80' : '#059669' }]}>
            📋 Past Orders ({(response.result as Order[]).length} items)
          </Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            <View style={styles.pastOrdersContainer}>
              {(response.result as Order[]).map((order, idx) => 
                renderOrderCard(order, idx)
              )}
            </View>
          </ScrollView>
        </View>
      )}
    </View>
  );

  const quickActions = [
    { text: "Find spicy veg food under 300₹", emoji: "🌶️" },
    { text: "Order chicken biryani", emoji: "🍛" },
    { text: "View my past orders", emoji: "📋" },
    { text: "Find non-veg food under 500₹", emoji: "🍖" }
  ];

  return (
    <View style={[
      styles.container,
      { backgroundColor: isDark ? '#181a20' : '#fff' }
    ]}>
      <View style={styles.headerContainer}>
        <Text style={[
          styles.heading,
          { color: isDark ? '#fff' : '#000' }
        ]}>🤖 AI Food Assistant</Text>
        
        {responses.length > 0 && (
          <TouchableOpacity
            style={[
              styles.clearButton,
              { backgroundColor: isDark ? '#dc2626' : '#ef4444' }
            ]}
            onPress={clearConversation}
          >
            <Text style={styles.clearButtonText}>Clear</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Input Area */}
      <View style={[
        styles.inputContainer,
        { backgroundColor: isDark ? '#23262f' : '#f8f9fa' }
      ]}>
        <TextInput
          style={[
            styles.input,
            {
              backgroundColor: isDark ? '#2a2d36' : '#fff',
              color: isDark ? '#fff' : '#000',
              borderColor: isDark ? '#444' : '#ddd',
            }
          ]}
          placeholder="Ask for food recommendations, place orders, or view history..."
          placeholderTextColor={isDark ? '#aaa' : '#888'}
          multiline
          value={input}
          onChangeText={setInput}
          maxLength={200}
        />
        
        <TouchableOpacity
          style={[
            styles.sendButton,
            { 
              backgroundColor: loading ? '#ccc' : '#ff6600',
              opacity: loading ? 0.6 : 1
            }
          ]}
          onPress={handleSubmit}
          disabled={loading || !input.trim()}
        >
          {loading ? (
            <ActivityIndicator size="small" color="#fff" />
          ) : (
            <Text style={styles.sendButtonText}>Send</Text>
          )}
        </TouchableOpacity>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActionsContainer}>
        <View style={styles.quickActionsGrid}>
          {quickActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.quickActionButton,
                { backgroundColor: isDark ? '#2a2d36' : '#f0f0f0' }
              ]}
              onPress={() => setInput(action.text)}
            >
              <Text style={styles.quickActionEmoji}>{action.emoji}</Text>
              <Text style={[
                styles.quickActionText,
                { color: isDark ? '#fff' : '#000' }
              ]}>{action.text}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* Chat History */}
      <ScrollView style={styles.chatContainer} showsVerticalScrollIndicator={false}>
        {responses.slice().reverse().map((response, index) => renderResponse(response, responses.length - 1 - index))}
      </ScrollView>
    </View>
  );
};

export default AIChatScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  headerContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 20,
    marginBottom: 16,
  },
  heading: {
    fontSize: 24,
    fontWeight: '700',
  },
  clearButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    backgroundColor: '#ef4444',
  },
  clearButtonText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  quickActionsContainer: {
    marginBottom: 16,
    paddingHorizontal: 20,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  quickActionButton: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    marginBottom: 8,
    borderRadius: 16,
    alignItems: 'center',
    width: '48%',
  },
  quickActionEmoji: {
    fontSize: 14,
    marginBottom: 2,
  },
  quickActionText: {
    fontSize: 10,
    textAlign: 'center',
    fontWeight: '500',
  },
  chatContainer: {
    flex: 1,
    paddingHorizontal: 20,
  },
  responseContainer: {
    marginBottom: 16,
    padding: 16,
    borderRadius: 12,
    backgroundColor: '#f4f4f4',
  },
  responseText: {
    fontSize: 16,
    fontWeight: '500',
    marginBottom: 12,
  },
  resultsContainer: {
    marginTop: 8,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 12,
  },
  restaurantCard: {
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    backgroundColor: '#f8f9fa',
  },
  restaurantName: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  restaurantDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  detailText: {
    fontSize: 12,
    color: '#666',
  },
  priceText: {
    fontSize: 14,
    fontWeight: '700',
    color: '#059669',
  },
  orderCard: {
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
    marginRight: 8,
    minWidth: 120,
    backgroundColor: '#f8f9fa',
  },
  orderDish: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 4,
  },
  orderQuantity: {
    fontSize: 12,
    color: '#666',
  },
  pastOrdersContainer: {
    flexDirection: 'row',
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 16,
    alignItems: 'flex-end',
    backgroundColor: '#f8f9fa',
    marginBottom: 16,
  },
  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginRight: 12,
    maxHeight: 100,
    backgroundColor: '#fff',
  },
  sendButton: {
    backgroundColor: '#ff6600',
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 20,
    minWidth: 60,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sendButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
});