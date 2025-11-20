""" JAC Learning Examples - Object-Spatial Programming (OSP) """

# This example introduces the core OSP concepts:
# - Nodes: Stateful entities holding data
# - Edges: Typed relationships between nodes
# - Walkers: Mobile computation that traverses the graph

# Define nodes for a social network
node Person {
    has name: str;
    has age: int;
    has interests: list[str] = [];
    has visited: bool = False;  # For tracking walker visits
}

# Define edges for relationships
edge FriendsWith {
    has since: str;
    has closeness: int;  # 1-10 scale
}

edge WorksWith {
    has company: str;
    has role: str;
}

# Define nodes for a simple knowledge graph
node Concept {
    has name: str;
    has description: str;
    has difficulty: int = 1;  # 1=beginner, 2=intermediate, 3=advanced
}

edge DependsOn {
    has prerequisite_level: int;  # How important this dependency is
}

# Walker for finding common interests between people
walker FindCommonInterests {
    has target_person: Person;
    has common_interests: list[str] = [];
    
    can find_matches with Person entry {
        if here == self.target_person {
            return;  # Don't compare with self
        }
        
        # Find shared interests
        shared: list[str] = [];
        for interest in here.interests {
            if interest in self.target_person.interests {
                shared.append(interest);
            }
        }
        
        if len(shared) > 0 {
            self.common_interests.extend(shared);
            print(f"🎯 {here.name} and {self.target_person.name} both like: {', '.join(shared)}");
        }
        
        # Continue to all connected people
        visit [-->];
    }
}

# Walker for greeting everyone in a network
walker GreetNetwork {
    can greet with Person entry {
        if not here.visited {
            here.visited = True;
            print(f"👋 Hello, {here.name}! Thanks for visiting our network.");
            
            # Continue to all connected people
            visit [--> ->:FriendsWith:->];
        }
    }
}

# Walker for learning path in knowledge graph
walker LearningPath {
    has target_concept: Concept;
    has prerequisites: list[Concept] = [];
    
    can find_dependencies with Concept entry {
        if here == self.target_concept {
            return;  # Don't include the target itself
        }
        
        if here not in self.prerequisites {
            self.prerequisites.append(here);
            print(f"📚 Prerequisite: {here.name} ({here.description})");
        }
        
        # Continue to dependent concepts
        visit [--> ->:DependsOn:->];
    }
}

with entry {
    print("=== Object-Spatial Programming Demo ===");
    print("Building a social network graph...\n");
    
    # Create people (nodes)
    alice = root ++> Person(name="Alice", age=25, interests=["coding", "music", "hiking"]);
    bob = root ++> Person(name="Bob", age=27, interests=["music", "sports", "cooking"]);
    charlie = root ++> Person(name="Charlie", age=24, interests=["coding", "gaming", "music"]);
    diana = root ++> Person(name="Diana", age=26, interests=["art", "photography", "travel"]);
    eve = root ++> Person(name="Eve", age=23, interests=["coding", "gaming", "reading"]);
    
    # Create friendships (edges) with metadata
    alice +>:FriendsWith(since="2020-01-15", closeness=8):+> bob;
    alice +>:FriendsWith(since="2021-06-10", closeness=9):+> charlie;
    bob +>:FriendsWith(since="2020-12-03", closeness=7):+> charlie;
    charlie +>:FriendsWith(since="2022-03-20", closeness=6):+> eve;
    alice +>:FriendsWith(since="2021-09-01", closeness=5):+> diana;
    
    print("Social network created!");
    print("People in network:");
    people = [root --> ->:FriendsWith:-> (`?Person)];
    for person in people {
        print(f"  • {person.name} (age {person.age})");
    }
    
    print(f"\nTotal connections: {len([root --> ->:FriendsWith:->])}");
}

with entry {
    print("\n=== Finding Common Interests ===");
    
    # Find all people Alice might be compatible with
    alice_friends = [root --> ->:FriendsWith:-> (`?Person)];
    finder = FindCommonInterests(target_person=alice_friends[0]);  # Alice is first
    
    print(f"Looking for people with similar interests to {alice_friends[0].name}:");
    for friend in alice_friends {
        friend spawn finder;
    }
    
    print(f"\nFound {len(finder.common_interests)} shared interests total!");
}

with entry {
    print("\n=== Greeting the Network ===");
    
    # Reset visited flags
    people = [root --> ->:FriendsWith:-> (`?Person)];
    for person in people {
        person.visited = False;
    }
    
    print("Starting greet walker from Alice...");
    greeter = GreetNetwork();
    alice = [root --> ->:FriendsWith:-> (`?Person)][0];  # Get Alice
    alice spawn greeter;
}

with entry {
    print("\n=== Social Network Analysis ===");
    
    # Find close friendships (closeness >= 8)
    close_friendships = [root --> ->:FriendsWith:closeness>=8:->];
    print(f"Close friendships (closeness >= 8): {len(close_friendships)}");
    
    for friendship in close_friendships {
        print(f"  🔗 {friendship[0].name} ↔ {friendship[1].name} (closeness: {friendship[2]})");
    }
    
    # Find music lovers
    music_lovers = [root --> ->:FriendsWith:-> (`?Person) 
                   -->:interests:{"music"}];
    print(f"\nPeople who like music: {len(music_lovers)}");
    for person in music_lovers {
        print(f"  🎵 {person.name}");
    }
    
    # Find coding enthusiasts
    coders = [root --> ->:FriendsWith:-> (`?Person) 
             -->:interests:{"coding"}];
    print(f"\nPeople who like coding: {len(coders)}");
    for person in coders {
        print(f"  💻 {person.name}");
    }
}

# Knowledge Graph Example
with entry {
    print("\n=== Knowledge Graph for Programming ===");
    
    # Create programming concepts
    programming = root ++> Concept(
        name="Programming",
        description="The art of creating computer programs",
        difficulty=1
    );
    
    python = root ++> Concept(
        name="Python",
        description="A high-level, interpreted programming language",
        difficulty=1
    );
    
    jac = root ++> Concept(
        name="JAC",
        description="Object-Spatial Programming Language",
        difficulty=2
    );
    
    algorithms = root ++> Concept(
        name="Algorithms",
        description="Step-by-step procedures for solving problems",
        difficulty=2
    );
    
    data_structures = root ++> Concept(
        name="Data Structures",
        description="Ways of organizing and storing data",
        difficulty=2
    );
    
    # Create dependencies
    python +>:DependsOn(prerequisite_level=3):+> programming;
    jac +>:DependsOn(prerequisite_level=2):+> programming;
    algorithms +>:DependsOn(prerequisite_level=3):+> programming;
    data_structures +>:DependsOn(prerequisite_level=2):+> programming;
    jac +>:DependsOn(prerequisite_level=1):+> python;
    
    print("Programming concepts and their dependencies created!");
}

with entry {
    print("\n=== Learning Path for JAC ===");
    
    jac_concept = [root --> (`?Concept) -->:name:"JAC"][0];
    learner = LearningPath(target_concept=jac_concept);
    
    print(f"Finding prerequisites for learning {jac_concept.name}:");
    jac_concept spawn learner;
    
    print(f"\nTotal prerequisites: {len(learner.prerequisites)}");
    for prereq in learner.prerequisites {
        difficulty_text = ["Beginner", "Intermediate", "Advanced"][prereq.difficulty - 1];
        print(f"  📖 {prereq.name} ({difficulty_text})");
    }
}

# Scale-Agnostic Programming Example
with entry {
    print("\n=== Scale-Agnostic Programming ===");
    print("The same code works for single user or millions!");
    
    # User profiles (automatically isolated per user)
    node UserProfile {
        has username: str;
        has bio: str = "";
        has preferences: dict[str, str] = {};
    }
    
    walker CreateUserProfile {
        has username: str;
        has bio: str;
        
        can create with `root entry {
            # 'root' automatically points to the current user's graph
            profile = root ++> UserProfile(
                username=self.username,
                bio=self.bio
            );
            print(f"✅ Created profile for {self.username}");
        }
    }
    
    walker ListUserProfiles {
        can list with `root entry {
            profiles = [root --> (`?UserProfile)];
            print(f"👥 Found {len(profiles)} user profiles:");
            for profile in profiles {
                print(f"  • {profile.username}: {profile.bio}");
            }
        }
    }
    
    # In a real multi-user system, each user gets their own isolated graph
    CreateUserProfile(username="alice_dev", bio="JAC enthusiast") spawn root;
    CreateUserProfile(username="bob_prog", bio="Python developer learning JAC") spawn root;
    
    ListUserProfiles() spawn root;
}

# Automatic Persistence Example
with entry {
    print("\n=== Automatic Persistence ===");
    print("Data is automatically saved - no database needed!");
    
    node Counter {
        has count: int = 0;
        has last_updated: str = "Never";
        
        def increment() -> None {
            self.count += 1;
            self.last_updated = "Just now";
            print(f"📊 Counter incremented: {self.count}");
        }
        
        def reset() -> None {
            self.count = 0;
            self.last_updated = "Just now";
            print("🔄 Counter reset to 0");
        }
    }
    
    # Get or create counter
    counters = [root --> (`?Counter)];
    counter: Counter;
    
    if not counters {
        counter = root ++> Counter();
        print("🆕 Created new counter");
    } else {
        counter = counters[0];
        print(f"📊 Found existing counter: {counter.count}");
    }
    
    # Use the counter
    counter.increment();
    counter.increment();
    counter.increment();
    
    print(f"Final count: {counter.count}");
    print("\n💾 This data would be automatically saved in a real JAC server!");
    print("Run 'jac serve examples/06_object_spatial.jac' to test persistence");
}

# Practice Exercise
with entry {
    print("\n=== Practice Exercise: Movie Recommendation System ===");
    
    node User {
        has name: str;
        has preferences: list[str] = [];
    }
    
    node Movie {
        has title: str;
        has genre: str;
        has rating: float;
    }
    
    edge Likes {
        has rating: int;  # User's rating of the movie
    }
    
    walker RecommendMovies {
        has target_user: User;
        has recommendations: list[Movie] = [];
        
        can recommend with User entry {
            if here == self.target_user {
                return;  # Skip self
            }
            
            # Find movies both users liked
            liked_by_target = [self.target_user --> ->:Likes:-> (`?Movie)];
            liked_by_current = [here --> ->:Likes:-> (`?Movie)];
            
            for movie in liked_by_current {
                if movie in liked_by_target {
                    if movie not in self.recommendations {
                        self.recommendations.append(movie);
                        print(f"🎬 Recommend '{movie.title}' ({movie.genre}) - {movie.rating}/10");
                    }
                }
            }
            
            visit [-->];  # Continue to next user
        }
    }
    
    # Create users and movies
    alice = root ++> User(name="Alice", preferences=["Action", "Sci-Fi"]);
    bob = root ++> User(name="Bob", preferences=["Drama", "Comedy"]);
    charlie = root ++> User(name="Charlie", preferences=["Action", "Comedy"]);
    
    inception = root ++> Movie(title="Inception", genre="Sci-Fi", rating=9.0);
    the_godfather = root ++> Movie(title="The Godfather", genre="Drama", rating=9.5);
    deadpool = root ++> Movie(title="Deadpool", genre="Action", rating=8.0);
    the_office = root ++> Movie(title="The Office", genre="Comedy", rating=8.5);
    
    # Create likes (Alice and Charlie both like action movies)
    alice +>:Likes(rating=9):+> inception;
    charlie +>:Likes(rating=8):+> inception;
    charlie +>:Likes(rating=9):+> deadpool;
    
    bob +>:Likes(rating=10):+> the_godfather;
    bob +>:Likes(rating=7):+> the_office;
    
    print("Movie recommendations for Alice:");
    recommender = RecommendMovies(target_user=alice);
    alice spawn recommender;
    
    if len(recommender.recommendations) == 0 {
        print("No recommendations found - need more user data!");
    }
}