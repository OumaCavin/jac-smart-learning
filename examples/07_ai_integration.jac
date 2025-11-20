""" JAC Learning Examples - AI Integration with byLLM """

# Note: This example requires byLLM to be set up properly
# You'll need to configure your LLM API key and model

# import from byllm.llm {Model};
# glob llm = Model(model_name="gpt-4o", verbose=False);

# For this example, we'll create a mock AI function
def smart_response(prompt: str) -> str {
    # Mock AI response - in real usage, this would use byLLM
    responses = {
        "hello": "Hello! I'm your AI assistant. How can I help you today?",
        "weather": "I don't have access to real-time weather data, but I'd recommend checking a weather app or website!",
        "coding": "Coding is amazing! JAC's Object-Spatial Programming makes complex data relationships much easier to handle.",
        "help": "I can help with programming questions, explain concepts, or just chat! What would you like to know?"
    };
    
    # Simple keyword matching for demo
    prompt_lower = prompt.lower();
    for keyword, response in responses.items() {
        if keyword in prompt_lower {
            return response;
        }
    }
    
    return f"That's an interesting question about '{prompt}'. I'd love to help you explore this topic further!";
}

# AI-Enhanced Chat Assistant
obj ChatAssistant {
    has conversation_history: list[dict[str, str]] = [];
    has user_preferences: dict[str, any] = {};
    
    def chat(message: str) -> str {
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message});
        
        # Process with AI (mock for demo)
        response = smart_response(message);
        
        # Add AI response to history
        self.conversation_history.append({"role": "assistant", "content": response});
        
        return response;
    }
    
    def get_context() -> str {
        if len(self.conversation_history) == 0 {
            return "No conversation history";
        }
        
        context = "Conversation context:\n";
        for entry in self.conversation_history[-5:] {  # Last 5 exchanges
            context += f"{entry["role"]}: {entry["content"]}\n";
        }
        return context;
    }
    
    def clear_history() -> None {
        self.conversation_history = [];
    }
}

# AI-Powered Code Assistant
obj CodeAssistant {
    has examples: dict[str, list[str]] = {
        "loops": [
            "for i = 0 to i < 10 by i += 1 { print(i); }",
            "while condition { /* code */ }",
            "for item in collection { /* process item */ }"
        ],
        "functions": [
            "def greet(name: str) -> str { return f\"Hello, {name}!\"; }",
            "def calculate_area(length: float, width: float) -> float { return length * width; }"
        ],
        "objects": [
            "obj Person { has name: str; has age: int; }",
            "impl Person.get_info { return f\"{self.name}, {self.age}\"; }"
        ]
    };
    
    def explain_concept(concept: str) -> str {
        explanations = {
            "variables": "Variables store data in JAC. Use type annotations like 'name: str = \"Alice\"' for clarity.",
            "loops": "JAC has for-to-by loops (for counting) and for-in loops (for iterating collections).",
            "functions": "Functions group code for reuse. Use 'def function_name(params) -> return_type { }'.",
            "objects": "Objects combine data (has) and behavior (def). Use impl blocks for implementations.",
            "nodes": "Nodes are graph entities in Object-Spatial Programming. Create them with 'root ++> NodeName()'.",
            "edges": "Edges connect nodes with typed relationships. Use '+>:EdgeType:+>' to create them.",
            "walkers": "Walkers traverse graphs performing computation. Use 'visit [-->]' to move between nodes."
        };
        
        concept_lower = concept.lower();
        for key, explanation in explanations.items() {
            if key in concept_lower {
                return explanation;
            }
        }
        
        return f"'{concept}' is a concept in JAC programming. I can explain variables, loops, functions, objects, nodes, edges, and walkers!";
    }
    
    def suggest_code(topic: str) -> str {
        if topic in self.examples {
            examples = self.examples[topic];
            return f"Here are some {topic} examples:\n" + "\n".join([f"• {example}" for example in examples]);
        }
        
        return f"I have examples for: {', '.join(self.examples.keys())}. Which topic interests you?";
    }
    
    def debug_code(code: str) -> str {
        common_issues = {
            "missing_semicolon": "Don't forget semicolons at the end of statements!",
            "missing_types": "Add type annotations like 'x: int = 5;' for better code.",
            "wrong_braces": "Use curly braces {} instead of indentation for code blocks.",
            "no_entry": "Wrap executable code in 'with entry { }' block."
        };
        
        code_lower = code.lower();
        if "def " in code_lower and "{" in code and "}" in code {
            if "with entry" not in code_lower {
                return "This function looks good! Make sure to wrap executable code in 'with entry { }'.";
            }
            return "The code structure looks correct! Check for any syntax errors.";
        }
        
        if not ("{" in code and "}" in code) {
            return "Missing curly braces {} for code blocks?";
        }
        
        if ":" not in code and "=" in code {
            return "Consider adding type annotations for better code clarity!";
        }
        
        return "The code looks mostly correct! Double-check for any remaining issues.";
    }
}

# AI-Enhanced Content Generator
obj ContentGenerator {
    has templates: dict[str, str] = {
        "welcome": "Welcome to our {platform}! We're excited to have you join our community.",
        "reminder": "Don't forget to {action} before {deadline}. You're doing great!",
        "achievement": "🎉 Congratulations! You've achieved {achievement}. Keep up the excellent work!"
    };
    
    def generate_content(template_name: str, **kwargs) -> str {
        if template_name not in self.templates {
            available = ", ".join(self.templates.keys());
            return f"Available templates: {available}";
        }
        
        template = self.templates[template_name];
        
        # Replace placeholders with provided values
        for key, value in kwargs.items() {
            placeholder = "{" + key + "}";
            template = template.replace(placeholder, str(value));
        }
        
        return template;
    }
    
    def create_personalized_message(user_name: str, activity: str, level: str) -> str {
        messages = {
            "beginner": f"Hey {user_name}! 👋 Great to see you starting with {activity}! Every expert was once a beginner.",
            "intermediate": f"Excellent progress, {user_name}! 🎯 Your {activity} skills are really coming together.",
            "advanced": f"Incredible work, {user_name}! 🏆 You're a true {activity} expert now!"
        };
        
        return messages.get(level, f"Keep up the great work with {activity}, {user_name}!");
    }
}

# AI-Powered Data Analyzer
obj DataAnalyzer {
    def analyze_sentiment(text: str) -> str {
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "like", "happy", "excited"];
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "sad", "angry", "frustrated", "disappointed"];
        
        text_lower = text.lower();
        positive_count = sum([1 for word in positive_words if word in text_lower]);
        negative_count = sum([1 for word in negative_words if word in text_lower]);
        
        if positive_count > negative_count {
            return f"Positive sentiment detected ({positive_count} positive vs {negative_count} negative words)";
        } elif negative_count > positive_count {
            return f"Negative sentiment detected ({negative_count} negative vs {positive_count} positive words)";
        } else {
            return f"Neutral sentiment ({positive_count} positive, {negative_count} negative words)";
        }
    }
    
    def extract_keywords(text: str, min_length: int = 4) -> list[str] {
        # Simple keyword extraction
        words = text.lower().split();
        keywords = [];
        
        for word in words {
            if len(word) >= min_length and word.isalpha() {
                if word not in ["this", "that", "with", "have", "will", "from", "they", "been", "were", "said"] {
                    keywords.append(word);
                }
            }
        }
        
        # Remove duplicates while preserving order
        unique_keywords = [];
        for keyword in keywords {
            if keyword not in unique_keywords {
                unique_keywords.append(keyword);
            }
        }
        
        return unique_keywords[:10];  # Return top 10
    }
    
    def summarize_text(text: str, max_sentences: int = 2) -> str {
        sentences = text.split(". ");
        if len(sentences) <= max_sentences {
            return text;
        }
        
        # Simple summarization - take first few sentences
        summary = ". ".join(sentences[:max_sentences]);
        if not summary.endswith(".") {
            summary += ".";
        }
        
        return f"Summary: {summary}";
    }
}

with entry {
    print("=== AI Integration Examples ===");
    print("Demonstrating AI-enhanced programming features...\n");
    
    # Chat Assistant Demo
    print("--- AI Chat Assistant ---");
    assistant = ChatAssistant();
    
    responses = [
        "Hello!",
        "Can you help me with programming?",
        "I love coding!",
        "What's the weather like?"
    ];
    
    for message in responses {
        response = assistant.chat(message);
        print(f"User: {message}");
        print(f"AI: {response}");
        print();
    }
    
    print("Conversation context:");
    print(assistant.get_context());
}

with entry {
    print("\n--- AI Code Assistant ---");
    code_assistant = CodeAssistant();
    
    # Concept explanations
    concepts = ["variables", "loops", "functions", "nodes and edges"];
    for concept in concepts {
        explanation = code_assistant.explain_concept(concept);
        print(f"📚 {concept.title()}: {explanation}");
        print();
    }
    
    # Code suggestions
    print("💡 Code Suggestions:");
    for topic in ["loops", "functions"] {
        suggestion = code_assistant.suggest_code(topic);
        print(f"{suggestion}\n");
    }
    
    # Code debugging
    print("🔍 Code Debugging:");
    debug_examples = [
        "def greet(name) { return f'Hello, {name}' }",  # Missing types
        "with entry { print('Hello world') }",          # Correct
        "if x > 5 { print('big') }"                    # Missing semicolons
    ];
    
    for i, code in enumerate(debug_examples, 1) {
        feedback = code_assistant.debug_code(code);
        print(f"Example {i}: {feedback}");
    }
}

with entry {
    print("\n--- AI Content Generator ---");
    generator = ContentGenerator();
    
    # Template-based generation
    print("📝 Content Generation:");
    messages = [
        generator.generate_content("welcome", platform="JAC Academy"),
        generator.generate_content("reminder", action="complete your assignment", deadline="Friday"),
        generator.generate_content("achievement", achievement="JAC Expert Badge")
    ];
    
    for message in messages {
        print(f"• {message}");
    }
    
    print();
    
    # Personalized messages
    print("🎯 Personalized Messages:");
    users = [
        ("Alice", "JAC programming", "beginner"),
        ("Bob", "graph algorithms", "intermediate"),
        ("Charlie", "AI integration", "advanced")
    ];
    
    for user_name, activity, level in users {
        message = generator.create_personalized_message(user_name, activity, level);
        print(f"• {message}");
    }
}

with entry {
    print("\n--- AI Data Analyzer ---");
    analyzer = DataAnalyzer();
    
    # Sentiment analysis
    texts = [
        "I absolutely love programming! It's amazing and wonderful.",
        "This is frustrating and terrible. I hate this code.",
        "The project is okay, some parts are good, others need work."
    ];
    
    print("😊 Sentiment Analysis:");
    for text in texts {
        sentiment = analyzer.analyze_sentiment(text);
        print(f"Text: '{text}'");
        print(f"Sentiment: {sentiment}\n");
    }
    
    # Keyword extraction
    print("🔑 Keyword Extraction:");
    sample_text = "JAC programming language offers object-spatial programming features that make graph data structures easier to handle and traverse.";
    keywords = analyzer.extract_keywords(sample_text);
    print(f"Text: '{sample_text}'");
    print(f"Keywords: {keywords}\n");
    
    # Text summarization
    print("📄 Text Summarization:");
    long_text = "JAC is a modern programming language that introduces Object-Spatial Programming (OSP). OSP allows computation to move to data instead of moving data to computation. This paradigm is particularly useful for handling graph-like data structures, social networks, and interconnected systems. The language supports both traditional programming concepts and advanced graph-based operations. JAC automatically handles persistence and provides built-in support for AI integration.";
    summary = analyzer.summarize_text(long_text, 2);
    print(f"Original: {long_text}");
    print(f"{summary}\n");
}

# Real-World AI Application: Smart Todo System
with entry {
    print("\n=== Real-World Application: Smart Todo System ===");
    
    node TodoItem {
        has title: str;
        has description: str = "";
        has completed: bool = False;
        has priority: int = 1;  # 1=Low, 2=Medium, 3=High
        has category: str = "General";
        has ai_enhanced: bool = False;
    }
    
    walker SmartTodoAssistant {
        has task_description: str;
        has priority: int = 1;
        has category: str = "General";
        
        can create_smart_todo with `root entry {
            # AI-enhanced task creation
            enhanced_title = smart_response(f"Create a concise title for: {self.task_description}");
            enhanced_description = smart_response(f"Provide a helpful description for: {self.task_description}");
            
            # Determine priority based on keywords
            if any(word in self.task_description.lower() for word in ["urgent", "important", "deadline", "asap"]) {
                self.priority = 3;
            } elif any(word in self.task_description.lower() for word in ["whenever", "sometime", "later"]) {
                self.priority = 1;
            } else {
                self.priority = 2;
            }
            
            todo = root ++> TodoItem(
                title=enhanced_title,
                description=enhanced_description,
                priority=self.priority,
                category=self.category,
                ai_enhanced=True
            );
            
            priority_text = ["Low", "Medium", "High"][self.priority - 1];
            print(f"✅ Created smart todo: {enhanced_title} [{priority_text}]");
            print(f"   Enhanced description: {enhanced_description}");
        }
    }
    
    walker TodoAnalyzer {
        can analyze_todos with `root entry {
            todos = [root --> (`?TodoItem)];
            
            if len(todos) == 0 {
                print("No todos found");
                return;
            }
            
            print(f"📊 Todo Analysis ({len(todos)} items):");
            
            # Analyze by priority
            priorities = {"High": 0, "Medium": 0, "Low": 0};
            for todo in todos {
                priority_text = ["Low", "Medium", "High"][todo.priority - 1];
                priorities[priority_text] += 1;
            }
            
            for priority, count in priorities.items() {
                print(f"  {priority} priority: {count}");
            }
            
            # AI insights
            high_priority_count = priorities["High"];
            if high_priority_count > len(todos) / 2 {
                print("💡 AI Insight: You have many high-priority items. Consider breaking some into smaller tasks.");
            } elif high_priority_count == 0 {
                print("💡 AI Insight: Great job on prioritizing! You might want to add more urgent tasks.");
            } else {
                print("💡 AI Insight: Your priority distribution looks balanced.");
            }
            
            # Find AI-enhanced todos
            ai_enhanced = [todo for todo in todos if todo.ai_enhanced];
            print(f"🤖 AI-enhanced todos: {len(ai_enhanced)}/{len(todos)}");
        }
    }
    
    # Create some smart todos
    SmartTodoAssistant(
        task_description="Complete the JAC programming tutorial by end of week",
        category="Learning",
        priority=3
    ) spawn root;
    
    SmartTodoAssistant(
        task_description="Review code and optimize performance when I have time",
        category="Development",
        priority=1
    ) spawn root;
    
    SmartTodoAssistant(
        task_description="Set up development environment for new project",
        category="Setup",
        priority=2
    ) spawn root;
    
    # Analyze the todos
    TodoAnalyzer() spawn root;
}

with entry {
    print("\n=== byLLM Setup Instructions ===");
    print("To use real AI features in JAC:");
    print("1. Install byLLM: pip install byllm");
    print("2. Get an API key from OpenAI, Anthropic, or Google");
    print("3. Configure your environment:");
    print("   export OPENAI_API_KEY='your-key-here'");
    print("4. Update the code to use real byLLM:");
    print("   glob llm = Model(model_name='gpt-4o')");
    print("   def ai_function() -> str byllm();");
    print("\nThis demo uses mock AI responses for illustration.");
    print("The real byLLM integration provides much more powerful AI capabilities!");
}