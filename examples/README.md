# JAC Programming Language - Interactive Learning Examples

This repository contains a comprehensive set of JAC programming language examples designed to take you from beginner to expert level through hands-on practice.

## 📚 Learning Path

### Phase 1: Foundation (Start Here!)
1. **[01_hello_world.jac](examples/01_hello_world.jac)** - Basic syntax, variables, and types
2. **[02_control_flow.jac](examples/02_control_flow.jac)** - If statements, loops, and conditions
3. **[03_functions.jac](examples/03_functions.jac)** - Functions, lambdas, and code organization
4. **[04_loops_collections.jac](examples/04_loops_collections.jac)** - Lists, dictionaries, sets, and iteration

### Phase 2: Object-Oriented Programming
5. **[05_oop.jac](examples/05_oop.jac)** - Classes, objects, methods, and interfaces

### Phase 3: Object-Spatial Programming (Advanced)
6. **[06_object_spatial.jac](examples/06_object_spatial.jac)** - Nodes, edges, walkers, and graph programming

### Phase 4: AI Integration (Expert)
7. **[07_ai_integration.jac](examples/07_ai_integration.jac)** - byLLM, AI assistants, and smart applications

## 🚀 Quick Start

### Prerequisites
- Python 3.12 or higher
- JAC language installed (`pip install -U jaclang`)

### Running Examples
```bash
# Run any example
jac run examples/01_hello_world.jac
jac run examples/02_control_flow.jac
# ... and so on

# For persistent examples (like object-spatial)
jac serve examples/06_object_spatial.jac
```

## 📖 What You'll Learn

### Beginner Level
- ✅ JAC syntax and basic structure
- ✅ Variables and type annotations
- ✅ Control flow (if/elif/else, loops)
- ✅ Functions and parameter handling
- ✅ Collections (lists, dictionaries, sets)

### Intermediate Level
- ✅ Object-Oriented Programming
- ✅ Classes, objects, and methods
- ✅ Interface/implementation separation
- ✅ Advanced control flow (pattern matching)
- ✅ Exception handling

### Advanced Level
- ✅ Object-Spatial Programming paradigm
- ✅ Graph-based data structures
- ✅ Nodes, edges, and walkers
- ✅ Scale-agnostic programming
- ✅ Automatic persistence

### Expert Level
- ✅ AI integration with byLLM
- ✅ Building intelligent applications
- ✅ Concurrent programming
- ✅ Production deployment

## 🎯 Practice Exercises

Each example includes practice exercises at the end. Try to solve them before looking at the solutions!

### Exercise Types
- **Basic**: Reinforce core concepts
- **Intermediate**: Apply multiple concepts together
- **Advanced**: Build complete applications
- **Expert**: Design complex systems

## 🏗️ Project Ideas to Build

### Beginner Projects
1. **Calculator** - Mathematical operations with functions
2. **Grade Book** - Manage student data with dictionaries
3. **Todo List** - Basic CRUD operations

### Intermediate Projects
4. **Library System** - Object-oriented design patterns
5. **Chat Bot** - Interactive conversation system
6. **Data Analyzer** - Process and analyze datasets

### Advanced Projects
7. **Social Network** - Graph-based relationships
8. **Recommendation Engine** - Intelligent suggestions
9. **Workflow System** - Complex business logic

### Expert Projects
10. **AI Assistant** - Natural language processing
11. **Distributed System** - Scale-agnostic architecture
12. **Full-Stack App** - Complete web application

## 🛠️ Development Setup

### 1. Install JAC
```bash
pip install -U jaclang
```

### 2. Verify Installation
```bash
jac --version
```

### 3. Set Up Your IDE
- **VS Code**: Install [Jac Extension](https://marketplace.visualstudio.com/items?itemName=jaseci-labs.jaclang-extension)
- **Cursor**: Install [Jac VSIX](https://github.com/Jaseci-Labs/jaseci/releases/latest)

### 4. Test Your Setup
```bash
echo "with entry { print('Hello, JAC!'); }" > test.jac
jac run test.jac
rm test.jac
```

## 📚 Additional Resources

### Official Documentation
- [JAC Language Reference](https://jac-lang.org/learn/jac_ref/)
- [Getting Started Guide](https://jac-lang.org/learn/getting_started/)
- [JAC in 5 Minutes](https://jac-lang.org/learn/jac_in_a_flash/)
- [Beginner's Guide](https://docs.jaseci.org/learn/beginners_guide_to_jac/)

### Community
- [GitHub Repository](https://github.com/Jaseci-Labs/jaclang)
- [Jaseci Documentation](https://docs.jaseci.org/)
- [JAC Playground](https://jac-lang.org/playground/)

## 🎓 Learning Tips

### Best Practices
1. **Start Small**: Begin with simple examples and gradually increase complexity
2. **Practice Daily**: Code every day, even if just for 15 minutes
3. **Build Projects**: Apply concepts to real-world problems
4. **Experiment**: Modify examples and see what happens
5. **Ask Questions**: Join the community for help and support

### Common Mistakes to Avoid
- ❌ Forgetting semicolons at the end of statements
- ❌ Omitting type annotations (they're recommended!)
- ❌ Using Python-style indentation instead of curly braces
- ❌ Missing `with entry` blocks for executable scripts
- ❌ Using `=` instead of `==` for comparison

### Study Schedule (Recommended)
- **Week 1-2**: Complete Examples 1-4 (Foundation)
- **Week 3-4**: Complete Example 5 (OOP) + practice projects
- **Week 5-6**: Complete Example 6 (Object-Spatial) + advanced projects
- **Week 7-8**: Complete Example 7 (AI Integration) + capstone project

## 🤖 AI Integration Setup (Advanced)

To use real AI features in JAC:

1. **Install byLLM**:
   ```bash
   pip install byllm
   ```

2. **Get an API Key**:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Google: https://makersuite.google.com/

3. **Configure Environment**:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   ```

4. **Update Examples**:
   ```jac
   import from byllm.llm {Model};
   glob llm = Model(model_name="gpt-4o");
   ```

## 🏆 Achievement Levels

Track your progress through these levels:

### 🥉 Bronze Level
- [ ] Run all 7 examples successfully
- [ ] Complete basic practice exercises
- [ ] Build 2-3 beginner projects

### 🥈 Silver Level
- [ ] Understand Object-Oriented Programming concepts
- [ ] Build a medium-sized application
- [ ] Contribute to community discussions

### 🥇 Gold Level
- [ ] Master Object-Spatial Programming
- [ ] Build a complex graph-based system
- [ ] Help other learners

### 💎 Expert Level
- [ ] Integrate AI into applications
- [ ] Build production-ready systems
- [ ] Contribute to JAC language development

## 📞 Getting Help

If you get stuck:

1. **Check the [Quick Reference Guide](../JAC_Quick_Reference.md)** for syntax help
2. **Review the [Complete Learning Guide](../JAC_Complete_Learning_Guide.md)** for detailed explanations
3. **Search the [Official Documentation](https://jac-lang.org/learn/)**
4. **Ask in the [GitHub Community](https://github.com/Jaseci-Labs/jaclang/discussions)**

## 🎉 What's Next?

After completing these examples:

1. **Build Your Own Project**: Choose something that interests you
2. **Join Open Source**: Contribute to JAC or related projects
3. **Teach Others**: Share your knowledge with the community
4. **Explore Advanced Topics**: Concurrent programming, performance optimization, etc.

Remember: **The best way to learn programming is by programming!** Start with these examples, but don't stop there. Build, experiment, and create amazing things with JAC!

---

**Happy Coding! 🚀**

*These examples are designed to complement the official JAC documentation. For the most up-to-date information, always refer to the [official documentation](https://jac-lang.org/)*