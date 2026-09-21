"""MIT EECS Distributed Systems & Algorithmic Foundations Curriculum Dataset.
Provides structured knowledge modules for Computer Science, Systems Engineering, and Research:
- 10 Course Lecture Sessions
- 8 Core Systems Concepts & Mechanisms
- 8 Key Technical Entities & Protocols
- 5 Comparative Differentials & Trade-off Syntheses
- 5 Critical Traps, Anti-Patterns & Pitfalls
- 25+ High-Yield Spaced-Repetition Active Recall Flashcards
"""

EECS_CURRICULUM_TOPICS = [
    {"name": "Distributed Consensus (Raft & Paxos Protocols)", "priority": "CRITICAL"},
    {"name": "Storage Engines (B-Trees vs LSM-Trees & Compaction)", "priority": "CRITICAL"},
    {"name": "Cache Coherence (MESI) & Memory Consistency Models", "priority": "HIGH"},
    {"name": "Transaction Recovery (WAL & ARIES Protocol)", "priority": "HIGH"},
    {"name": "Scalable Network I/O (Linux Epoll vs Select/Poll)", "priority": "MEDIUM"},
    {"name": "Virtual Memory, Page Tables & TLB Architecture", "priority": "MEDIUM"}
]

EECS_SESSIONS = [
    {
        "session_num": 1,
        "slug": "session-01-enforced-modularity-and-rpc",
        "title": "Session 01: Enforced Modularity, Client-Server & Remote Procedure Calls (RPC)",
        "instructors": "Prof. Robert Morris, Prof. Frans Kaashoek",
        "summary": "Architectural principles of enforced modularity using hardware virtual memory and client-server network boundaries.",
        "content": """### Session Objectives
1. Understand why soft modularity (function calls) fails to prevent fate-sharing and memory corruption.
2. Master hardware-enforced modularity via virtual memory address spaces and supervisor mode.
3. Analyze remote procedure calls (RPC): marshalling, network latency, at-least-once vs at-most-once semantics.

### Key Architectural Insights
- **Fate-sharing**: In a monolithic address space, an out-of-bounds pointer in one module corrupts the entire system.
- **Client-Server RPC Model**: Converts in-memory function calls into serialized network messages over sockets.
- **RPC Semantics**:
  - *At-least-once*: Client retries on timeout; requires idempotent handlers (e.g. read operations).
  - *At-most-once*: Server caches request IDs and responses to suppress duplicate execution of non-idempotent operations.

Related: [[entities/grpc-protobuf]], [[concepts/epoll-scalable-io-multiplexing]]."""
    },
    {
        "session_num": 2,
        "slug": "session-02-virtual-memory-paging-and-tlb",
        "title": "Session 02: Virtual Memory Architecture, Multi-Level Page Tables & TLB",
        "instructors": "Prof. Frans Kaashoek",
        "summary": "Hardware-software boundary of virtual memory translation, page faults, and translation lookaside buffer (TLB) shootdowns.",
        "content": """### Session Objectives
1. Derive multi-level page table walk overhead in x86-64 4-level paging (PML4).
2. Understand Translation Lookaside Buffer (TLB) caching and hardware page table walkers.
3. Analyze inter-processor interrupt (IPI) overhead in multi-core TLB shootdowns.

### Key Architectural Insights
- Virtual addresses provide isolation, address space relocation, and demand paging.
- Multi-level page tables save RAM for sparse address spaces, but require 4 memory reads per un-cached access.
- TLB hit rates (>99%) are critical for CPU pipeline throughput.

Related: [[concepts/virtual-memory-and-tlb]], [[entities/translation-lookaside-buffer-tlb]]."""
    },
    {
        "session_num": 3,
        "slug": "session-03-concurrency-locks-and-deadlock-prevention",
        "title": "Session 03: Concurrency Control, Spinlocks, Mutexes & Deadlock Prevention",
        "instructors": "Prof. Nickolai Zeldovich",
        "summary": "Mutual exclusion primitives, cache-coherence traffic under lock contention, and Coffman deadlock conditions.",
        "content": """### Session Objectives
1. Compare test-and-set spinlocks against ticket locks and MCS queue locks.
2. Prevent deadlocks by eliminating Coffman conditions via strict global lock acquisition ordering.
3. Understand reader-writer lock writer-starvation mitigation.

### Key Architectural Insights
- Test-and-set locks cause $O(N^2)$ bus invalidation traffic on multicore systems.
- Deadlock requires four simultaneous Coffman conditions: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.
- Lock ordering breaks the Circular Wait condition.

Related: [[concepts/two-phase-locking-vs-occ]], [[exam_traps/aba-problem-in-lockfree-concurrency]]."""
    },
    {
        "session_num": 4,
        "slug": "session-04-write-ahead-logging-and-recovery",
        "title": "Session 04: Crash Recovery, Write-Ahead Logging (WAL) & ARIES Protocol",
        "instructors": "Prof. Robert Morris",
        "summary": "Atomicity and durability guarantees in database engines via write-ahead logging, compensation log records, and checkpoints.",
        "content": """### Session Objectives
1. Master the write-ahead logging invariant: log records must reach non-volatile storage before dirty data pages.
2. Understand the ARIES recovery phases: Analysis, Redo, and Undo.
3. Analyze fuzzy checkpointing to minimize recovery time after an ungraceful crash.

### Key Architectural Insights
- The WAL protocol decouples transaction commit latency (append-only log flush) from disk seek latency (random in-place updates).
- Compensation Log Records (CLRs) ensure that crashes during recovery do not cause infinite recovery loops.

Related: [[concepts/write-ahead-logging-and-recovery]], [[entities/write-ahead-log-wal]]."""
    },
    {
        "session_num": 5,
        "slug": "session-05-distributed-consensus-and-paxos",
        "title": "Session 05: Distributed Consensus: The Paxos Protocol",
        "instructors": "Prof. Robert Morris",
        "summary": "Reaching consensus in asynchronous distributed networks with unreliable messaging: Multi-Paxos architecture.",
        "content": """### Session Objectives
1. Understand the consensus problem in asynchronous networks under crash-stop failure models.
2. Trace Phase 1 (Prepare/Promise) and Phase 2 (Accept/Accepted) in single-degree Paxos.
3. Analyze Multi-Paxos leader election and log synchronization.

### Key Architectural Insights
- Overlapping quorums ensure that any majority contains at least one node with the latest accepted value.
- Paxos guarantees Safety (no two nodes learn conflicting decisions) under arbitrary packet loss and delay.

Related: [[differentials/raft-vs-multi-paxos]], [[concepts/raft-distributed-consensus]]."""
    },
    {
        "session_num": 6,
        "slug": "session-06-raft-consensus-leader-election-and-logs",
        "title": "Session 06: The Raft Consensus Protocol: Leader Election & Log Replication",
        "instructors": "Prof. Frans Kaashoek",
        "summary": "Understandable consensus via decomposed leader election, log matching invariants, and randomized election timeouts.",
        "content": """### Session Objectives
1. Deconstruct consensus into three independent sub-problems: Leader Election, Log Replication, and Safety.
2. Master the Log Matching Invariant and how leader append-only enforcement resolves log divergences.
3. Analyze quorum configurations and randomized election timeouts to prevent split-vote livelocks.

### Key Architectural Insights
- Raft guarantees that the candidate with the most up-to-date log (higher term, longer log) wins the election.
- Leaders never overwrite or truncate their own logs; follower logs are forced to mirror the leader.

Related: [[concepts/raft-distributed-consensus]], [[entities/raft-leader-election]], [[entities/etcd]]."""
    },
    {
        "session_num": 7,
        "slug": "session-07-storage-engines-btrees-vs-lsm-trees",
        "title": "Session 07: Storage Engines: B+Trees vs Log-Structured Merge (LSM) Trees",
        "instructors": "Prof. Sam Madden",
        "summary": "Write amplification, read amplification, and compaction algorithms in modern database storage engines.",
        "content": """### Session Objectives
1. Compare B+Tree in-place page modification against LSM-Tree append-only SSTable flushing.
2. Analyze write amplification factor (WAF) and read amplification factor (RAF) under write-heavy workloads.
3. Understand leveled compaction vs size-tiered compaction in RocksDB.

### Key Architectural Insights
- B+Trees optimize for point reads ($O(\\log_B N)$) but incur heavy random writes.
- LSM-Trees convert random writes into sequential memory appends (MemTable) and background compactions.

Related: [[differentials/b-trees-vs-lsm-trees]], [[concepts/log-structured-merge-trees]], [[entities/rocksdb-lsm-store]]."""
    },
    {
        "session_num": 8,
        "slug": "session-08-cache-coherence-and-memory-models",
        "title": "Session 08: Cache Coherence (MESI/MOESI), Memory Barriers & Consistency",
        "instructors": "Prof. Arvind",
        "summary": "Hardware snooping protocols, write-invalidate vs write-update, store buffers, and sequential consistency.",
        "content": """### Session Objectives
1. Master the 4 states of the MESI protocol: Modified, Exclusive, Shared, Invalid.
2. Understand store buffers and memory barriers (acquire/release vs sequential consistency).
3. Diagnose false sharing performance degradation in multi-threaded programs.

### Key Architectural Insights
- Hardware cache coherence guarantees that all cores observe a single consistent view of each individual memory address.
- Store buffers allow CPU execution to proceed before L1 write invalidations finish, introducing memory reordering.

Related: [[concepts/cache-coherence-mesi-protocol]], [[entities/mesi-protocol]], [[exam_traps/false-sharing-in-multicore-cache-lines]]."""
    },
    {
        "session_num": 9,
        "slug": "session-09-scalable-network-io-epoll",
        "title": "Session 09: Scalable Event-Driven Network I/O: Select, Poll, and Epoll",
        "instructors": "Prof. Robert Morris",
        "summary": "Solving the C10K problem using kernel event notification subsystems (Linux Epoll, FreeBSD Kqueue).",
        "content": """### Session Objectives
1. Analyze the $O(N)$ linear scanning bottleneck in `select()` and `poll()`.
2. Trace the $O(1)$ red-black tree and ready-list architecture of Linux `epoll`.
3. Compare level-triggered (LT) and edge-triggered (ET) notification semantics.

### Key Architectural Insights
- `epoll` maintains state in kernel memory across invocations, eliminating $O(N)$ file descriptor array copying per event loop cycle.
- Edge-triggered mode notifies the application only when state changes, requiring non-blocking loops until `EAGAIN`.

Related: [[concepts/epoll-scalable-io-multiplexing]], [[differentials/level-triggered-vs-edge-triggered-epoll]], [[entities/epoll]]."""
    },
    {
        "session_num": 10,
        "slug": "session-10-cap-theorem-and-distributed-fault-tolerance",
        "title": "Session 10: Fault-Tolerance, Byzantine Failures & The CAP / PACELC Theorem",
        "instructors": "Prof. Frans Kaashoek",
        "summary": "Fundamental impossibility results in distributed systems: FLP theorem, CAP theorem, and practical consistency models.",
        "content": """### Session Objectives
1. Understand the CAP Theorem: under network partition ($P$), a distributed system must choose between Consistency ($C$) and Availability ($A$).
2. Extend CAP with the PACELC formulation: If partitioned, choose $A$ or $C$; else, choose Latency ($L$) or Consistency ($C$).
3. Compare crash-fault tolerance (CFT) with Byzantine fault tolerance (BFT).

### Key Architectural Insights
- True partitions cannot be avoided in physical networks; network timeouts cannot distinguish slow nodes from dead nodes.
- Systems choose CP (e.g. etcd, ZooKeeper) or AP (e.g. DynamoDB, Cassandra) depending on durability invariants.

Related: [[concepts/cap-theorem-and-pacelc]], [[concepts/raft-distributed-consensus]]."""
    }
]

EECS_CONCEPTS = [
    {
        "slug": "raft-distributed-consensus",
        "title": "Raft Distributed Consensus Protocol",
        "domain": "Computer Science",
        "field": "Distributed Systems",
        "course": "MIT 6.033",
        "tags": ["distributed-systems", "consensus", "fault-tolerance", "etcd"],
        "summary": "A leader-driven distributed consensus algorithm designed for understandability, dividing consensus into election, replication, and safety.",
        "content": """### Theoretical Foundation & Mechanism
Raft reaches consensus among $2F + 1$ distributed nodes, tolerating up to $F$ crash failures. Nodes exist in one of three states: **Leader**, **Follower**, or **Candidate**. Time is structured into logical **terms** (monotonically increasing integers acting as logical clocks).

```
[Follower] --(election timeout)--> [Candidate] --(majority votes)--> [Leader]
    ^                                     |                              |
    |------------(discovers higher term)--+------------------------------|
```

### Core Invariants & Guarantees
1. **Election Safety**: At most one leader can be elected per term.
2. **Leader Append-Only**: A leader never overwrites or truncates its log entries; it only appends new entries.
3. **Log Matching Property**: If two logs contain an entry with the same index and term, they are identical up to that index.
4. **Leader Completeness**: If a log entry is committed in a given term, that entry will be present in the logs of the leaders for all higher terms.
5. **State Machine Safety**: If a server has applied an entry at a given index to its state machine, no other server will ever apply a different entry for the same index.

### Critical Engineering Traps & Anti-Patterns
> [!CAUTION]
> **Even-Numbered Cluster Configurations**:
> Configuring an even number of nodes (e.g. 4 or 6) provides **zero** additional fault tolerance over $N-1$ nodes! A 4-node cluster requires 3 nodes for a majority quorum ($Q = \\lfloor 4/2 \\rfloor + 1 = 3$), allowing only 1 failure—identical to a 3-node cluster, while increasing the probability of split votes and network partitions.

Related: [[entities/etcd]], [[entities/raft-leader-election]], [[differentials/raft-vs-multi-paxos]], [[exam_traps/split-brain-consensus-even-quorum]]."""
    },
    {
        "slug": "log-structured-merge-trees",
        "title": "Log-Structured Merge (LSM) Trees & Compaction",
        "domain": "Computer Science",
        "field": "Storage Engines",
        "course": "MIT 6.033",
        "tags": ["storage", "databases", "rocksdb", "lsm-tree", "write-amplification"],
        "summary": "Storage architecture optimized for high-throughput write workloads by converting random disk writes into sequential append-only operations.",
        "content": """### Core Architecture & Mechanism
LSM-Trees buffer incoming writes in an in-memory balanced tree (**MemTable**, typically a SkipList), backed by an append-only **Write-Ahead Log (WAL)** for crash durability. When the MemTable reaches its memory limit, it is flushed as an immutable, sorted string table (**SSTable**) to disk at Level 0 ($L_0$).

```
Writes --> [WAL (Disk)] + [MemTable (RAM SkipList)]
                                |
                             (Flush)
                                v
               Level 0 SSTables (Key ranges overlap)
                                |
                           (Compaction)
                                v
               Level 1 SSTables (Disjoint sorted key ranges)
```

### Compaction Strategies
- **Size-Tiered Compaction**: Merges SSTables of similar sizes into larger SSTables; low write amplification but high space amplification.
- **Leveled Compaction (RocksDB)**: Each level $L_{i}$ has a total size limit ($10\\times$ larger than $L_{i-1}$). Key ranges within $L_{\\ge 1}$ are strictly non-overlapping, minimizing read amplification.
- **Bloom Filters**: Placed in memory for each SSTable to answer point queries in $O(1)$ without disk I/O when a key does not exist.

Related: [[entities/rocksdb-lsm-store]], [[differentials/b-trees-vs-lsm-trees]], [[concepts/write-ahead-logging-and-recovery]]."""
    },
    {
        "slug": "cache-coherence-mesi-protocol",
        "title": "Cache Coherence: The MESI Protocol & Store Buffers",
        "domain": "Computer Science",
        "field": "Computer Architecture",
        "course": "MIT 6.004",
        "tags": ["hardware", "architecture", "caching", "concurrency"],
        "summary": "Hardware snooping protocol that maintains coherence across per-core private CPU caches using Modified, Exclusive, Shared, and Invalid states.",
        "content": """### Protocol State Machine
Every cache line (typically 64 bytes) is tracked by a 2-bit state tag:
- **Modified (M)**: Line is present only in current core's cache and is dirty (memory holds stale value). Core has exclusive read/write permission.
- **Exclusive (E)**: Line is present only in current core's cache and is clean (matches memory). Core has exclusive write permission.
- **Shared (S)**: Line is present in current core's cache and potentially other cores' caches; clean. Read-only access.
- **Invalid (I)**: Line does not contain valid data.

### Store Buffers & Memory Barriers
To prevent CPU pipelines from stalling while waiting for *Read With Intent To Modify (RWITM)* invalidation acknowledgments from other cores, processors buffer writes into a **Store Buffer**.
- Store buffers break strict sequential consistency: writes become visible locally before invalidations propagate globally.
- Software **Memory Barriers** (`mfence`, `smp_mb()`) force the store buffer to drain before subsequent instructions proceed.

Related: [[entities/mesi-protocol]], [[exam_traps/false-sharing-in-multicore-cache-lines]], [[concepts/two-phase-locking-vs-occ]]."""
    },
    {
        "slug": "write-ahead-logging-and-recovery",
        "title": "Write-Ahead Logging (WAL) & ARIES Crash Recovery",
        "domain": "Computer Science",
        "field": "Database Systems",
        "course": "MIT 6.033",
        "tags": ["databases", "durability", "transactions", "wal"],
        "summary": "Fundamental transaction durability protocol ensuring Atomicity and Durability (ACID) via the write-ahead logging rule.",
        "content": """### The WAL Invariant
> **The Write-Ahead Logging Rule**:
> 1. Any log record describing an update to a database page must be flushed to non-volatile storage **before** the dirty database page itself is written to disk.
> 2. All log records for a transaction must be flushed before the transaction is acknowledged as committed (Commit Rule).

### ARIES Recovery Algorithm (3 Passes)
1. **Analysis Pass**: Scans forward from the last checkpoint to identify dirty pages in the buffer pool (Dirty Page Table) and active uncommitted transactions (Transaction Table).
2. **Redo Pass**: Repeats history by scanning forward from the smallest `RecLSN`, replaying all logged actions (including updates of rolled-back transactions) to restore the state at crash time.
3. **Undo Pass**: Scans backward, undoing the changes of all transactions that were active at the crash, writing **Compensation Log Records (CLRs)** to guarantee idempotent recovery if another crash occurs.

Related: [[entities/write-ahead-log-wal]], [[differentials/optimistic-vs-pessimistic-concurrency]]."""
    },
    {
        "slug": "epoll-scalable-io-multiplexing",
        "title": "Linux Epoll: Scalable Event-Driven Network Architecture",
        "domain": "Computer Science",
        "field": "Systems Programming",
        "course": "MIT 6.033",
        "tags": ["networking", "linux", "concurrency", "epoll", "c10k"],
        "summary": "Kernel-space event notification mechanism resolving the C10K linear scaling bottleneck of select and poll.",
        "content": """### Architectural Architecture & Kernel Data Structures
Linux `epoll` maintains two internal kernel data structures:
1. **Interest List (Red-Black Tree)**: Stores all registered file descriptors and their requested event masks ($O(\\log N)$ insertion, search, and deletion).
2. **Ready List (Doubly-Linked List)**: Stores only the file descriptors that have active I/O events ready, populated asynchronously by device driver interrupts.

$$\\text{select()/poll() Complexity: } O(N) \\quad \\longrightarrow \\quad \\text{epoll\\_wait() Complexity: } O(\\text{events})$$

### Level-Triggered vs Edge-Triggered
- **Level-Triggered (Default)**: `epoll_wait()` returns a descriptor repeatedly as long as buffer data remains unread. Safe and intuitive.
- **Edge-Triggered (EPOLLET)**: `epoll_wait()` notifies the application *only when state transitions* from unready to ready. Requires looping with non-blocking reads until `EAGAIN` or `EWOULDBLOCK`.

Related: [[entities/epoll]], [[differentials/level-triggered-vs-edge-triggered-epoll]], [[exam_traps/epoll-starvation-edge-triggered]]."""
    },
    {
        "slug": "virtual-memory-and-tlb",
        "title": "Virtual Memory, Multi-Level Page Tables & TLB Translation",
        "domain": "Computer Science",
        "field": "Computer Architecture",
        "course": "MIT 6.004",
        "tags": ["architecture", "operating-systems", "virtual-memory", "tlb"],
        "summary": "Hardware address translation mechanism isolating process memory spaces and enabling demand-paged execution.",
        "content": """### Address Translation Mechanism (x86-64)
In 64-bit x86 architecture (48-bit canonical virtual address), a 4-level page table hierarchy divides the 48-bit address into:
- 9 bits: Page Map Level 4 (PML4)
- 9 bits: Page Directory Pointer Table (PDPT)
- 9 bits: Page Directory (PD)
- 9 bits: Page Table (PT)
- 12 bits: Physical Page Offset ($2^{12} = 4096$ bytes)

### Translation Lookaside Buffer (TLB)
The TLB is a high-speed, fully associative or set-associative cache located on the CPU core holding virtual-to-physical address mappings.
- **TLB Hit**: Address translation completes in 1 clock cycle.
- **TLB Miss**: Requires 4 sequential main memory accesses to traverse the page table hierarchy.
- **TLB Shootdown**: When a multi-threaded process modifies a page table mapping, the operating system must send Inter-Processor Interrupts (IPI) to all other cores running threads of that process to invalidate their local TLB entries.

Related: [[entities/translation-lookaside-buffer-tlb]], [[concepts/cache-coherence-mesi-protocol]]."""
    },
    {
        "slug": "cap-theorem-and-pacelc",
        "title": "CAP Theorem & The PACELC Trade-Off Formulation",
        "domain": "Computer Science",
        "field": "Distributed Systems",
        "course": "MIT 6.033",
        "tags": ["distributed-systems", "theory", "cap-theorem", "consistency"],
        "summary": "Fundamental trade-offs between consistency, availability, and latency in partitioned distributed storage networks.",
        "content": """### The CAP Formulation (Eric Brewer)
In any distributed asynchronous data store subject to network partitions ($P$):
- **Consistency ($C$)**: Every read receives the most recent write or an error (Linearizability).
- **Availability ($A$)**: Every non-failing node returns a non-error response for every request, without guarantee that it contains the most recent write.
- **Partition Tolerance ($P$)**: The system continues to operate despite arbitrary message loss or delay.

Since physical networks inevitably experience partitions ($P$), systems must make a trade-off between **$CP$** (reject writes/reads to preserve safety, e.g., Raft/etcd) and **$AP$** (serve stale data to maintain uptime, e.g., Cassandra/Dynamo).

### The PACELC Extension (Daniel Abadi)
If there is a Partition ($P$):
- Trade off **Availability ($A$)** vs **Consistency ($C$)**;
Else ($E$):
- Trade off **Latency ($L$)** vs **Consistency ($C$)**.

Related: [[concepts/raft-distributed-consensus]], [[differentials/raft-vs-multi-paxos]]."""
    },
    {
        "slug": "two-phase-locking-vs-occ",
        "title": "Concurrency Control: Two-Phase Locking (2PL) vs OCC",
        "domain": "Computer Science",
        "field": "Database Systems",
        "course": "MIT 6.033",
        "tags": ["databases", "concurrency", "transactions", "serializability"],
        "summary": "Comparative concurrency control paradigms guaranteeing conflict serializability under varying workload contention.",
        "content": """### Strict Two-Phase Locking (SS2PL) - Pessimistic
- **Growing Phase**: Transaction acquires shared locks (reads) or exclusive locks (writes). Once a lock is released, no new locks can be acquired.
- **Strict Rule**: All exclusive locks must be held until the transaction finishes (commit or abort) to prevent cascading aborts.
- **Trade-off**: High lock overhead and deadlock risk under high contention; zero wasted work on commit.

### Optimistic Concurrency Control (OCC) - Kung-Robinson
Transactions proceed without taking locks across three phases:
1. **Read Phase**: Reads from database; writes are buffered in private local workspace.
2. **Validation Phase**: Checks whether transaction's read set conflicts with write sets of concurrently committed transactions.
3. **Write Phase**: If validation passes, local writes are applied to the database; if validation fails, transaction aborts and restarts.

Related: [[differentials/optimistic-vs-pessimistic-concurrency]], [[concepts/write-ahead-logging-and-recovery]]."""
    }
]

EECS_ENTITIES = [
    {
        "slug": "etcd",
        "title": "etcd (Distributed Key-Value Store)",
        "domain": "Computer Science",
        "category": "distributed-system",
        "course": "MIT 6.033",
        "summary": "A strongly consistent, distributed key-value store implementing Raft, used as the source of truth for Kubernetes cluster state.",
        "content": """### High-Yield Technical Notes
- Implements the **Raft consensus algorithm** in Go.
- Provides linearizable reads, multi-version concurrency control (MVCC), and long-lived watch streams via gRPC.
- Storage backend is **bbolt** (an embedded, ACID-compliant B+Tree).
- Critical for Kubernetes control plane: coordinates leader election, pod scheduling, and configuration manifests.

Related: [[concepts/raft-distributed-consensus]], [[entities/grpc-protobuf]]."""
    },
    {
        "slug": "epoll",
        "title": "epoll (Linux Event Notification Subsystem)",
        "domain": "Computer Science",
        "category": "kernel-subsystem",
        "course": "MIT 6.033",
        "summary": "High-performance Linux kernel facility for monitoring multiple file descriptors to see if I/O is possible.",
        "content": """### High-Yield Technical Notes
- System calls: `epoll_create1(flags)`, `epoll_ctl(epfd, op, fd, event)`, and `epoll_wait(epfd, events, maxevents, timeout)`.
- Replaces $O(N)$ scanning with an $O(1)$ ready list populated by kernel socket state change interrupts.
- Powers Nginx, Node.js (libuv), Redis, and Go netpoller.

Related: [[concepts/epoll-scalable-io-multiplexing]], [[differentials/level-triggered-vs-edge-triggered-epoll]]."""
    },
    {
        "slug": "translation-lookaside-buffer-tlb",
        "title": "Translation Lookaside Buffer (TLB)",
        "domain": "Computer Science",
        "category": "hardware-component",
        "course": "MIT 6.004",
        "summary": "A specialized hardware cache within the CPU memory management unit (MMU) that stores recent virtual-to-physical address translations.",
        "content": """### High-Yield Technical Notes
- Reduces multi-level page table traversal overhead from 4 memory accesses down to 1 CPU cycle on a hit.
- Split into instruction TLB (iTLB) and data TLB (dTLB).
- TLB entries are tagged with Address Space Identifiers (ASID/PCID) to prevent complete flushes on context switches.

Related: [[concepts/virtual-memory-and-tlb]], [[concepts/cache-coherence-mesi-protocol]]."""
    },
    {
        "slug": "write-ahead-log-wal",
        "title": "Write-Ahead Log (WAL)",
        "domain": "Computer Science",
        "category": "storage-structure",
        "course": "MIT 6.033",
        "summary": "An append-only disk log file recording state changes prior to applying modifications to in-place database structures.",
        "content": """### High-Yield Technical Notes
- Guarantees durability ($D$) in ACID transactions without requiring synchronous random disk I/O on every commit.
- Uses Log Sequence Numbers (LSN) to strictly order operations.
- Flushed via `fsync()` system call before returning success to user clients.

Related: [[concepts/write-ahead-logging-and-recovery]], [[concepts/log-structured-merge-trees]]."""
    },
    {
        "slug": "raft-leader-election",
        "title": "Raft Leader Election Protocol",
        "domain": "Computer Science",
        "category": "consensus-algorithm",
        "course": "MIT 6.033",
        "summary": "The leader election sub-protocol in Raft using randomized timeouts and RequestVote RPCs to guarantee single-leader safety.",
        "content": """### High-Yield Technical Notes
- Uses randomized election timeouts (typically 150ms–300ms) to prevent split-vote livelocks.
- Voters only grant votes if candidate's log is at least as up-to-date as the voter's own log:
  $$\\text{Candidate Term} > \\text{Voter Term} \\quad \\lor \\quad (\\text{Term Match} \\land \\text{Candidate Log Length} \\ge \\text{Voter Log Length})$$

Related: [[concepts/raft-distributed-consensus]], [[exam_traps/split-brain-consensus-even-quorum]]."""
    },
    {
        "slug": "rocksdb-lsm-store",
        "title": "RocksDB (LSM-Tree Embedded Storage Engine)",
        "domain": "Computer Science",
        "category": "storage-engine",
        "course": "MIT 6.033",
        "summary": "High-performance embedded key-value database developed by Meta, built on the Log-Structured Merge (LSM) Tree pattern.",
        "content": """### High-Yield Technical Notes
- Forked from Google's LevelDB, optimized for multicore CPU utilization and NVMe SSD bandwidth.
- Architecture: MemTable (RAM SkipList) $\\to$ WAL (Disk) $\\to$ Leveled SSTables with Block Cache and Bloom Filters.
- Underlies Kafka Streams, CockroachDB, TiKV, and Ceph.

Related: [[concepts/log-structured-merge-trees]], [[differentials/b-trees-vs-lsm-trees]]."""
    },
    {
        "slug": "grpc-protobuf",
        "title": "gRPC & Protocol Buffers",
        "domain": "Computer Science",
        "category": "network-framework",
        "course": "MIT 6.033",
        "summary": "Modern open source high-performance remote procedure call (RPC) framework based on HTTP/2 transport and binary Protocol Buffers.",
        "content": """### High-Yield Technical Notes
- Binary wire serialization via Protobuf produces $3-10\\times$ smaller payloads and faster serialization than JSON.
- Multiplexes bidirectional streaming calls over a single persistent TCP connection via HTTP/2 frames.
- Replaces legacy CORBA and Java RMI with cross-language contract enforcement (`.proto`).

Related: [[session-01-enforced-modularity-and-rpc]], [[differentials/tcp-vs-udp-transport]]."""
    },
    {
        "slug": "mesi-protocol",
        "title": "MESI Hardware Cache Protocol",
        "domain": "Computer Science",
        "category": "hardware-protocol",
        "course": "MIT 6.004",
        "summary": "Write-invalidate cache coherence protocol used in symmetric multiprocessing (SMP) systems.",
        "content": """### High-Yield Technical Notes
- Four discrete states: Modified, Exclusive, Shared, Invalid.
- Solves the multicore stale read problem by snooping the shared system bus.
- Write hits to Shared (S) lines broadcast an Invalidation signal, transitioning the line to Modified (M) and all peer caches to Invalid (I).

Related: [[concepts/cache-coherence-mesi-protocol]], [[exam_traps/false-sharing-in-multicore-cache-lines]]."""
    }
]

EECS_DIFFERENTIALS = [
    {
        "slug": "raft-vs-multi-paxos",
        "title": "Raft vs Multi-Paxos Distributed Consensus",
        "summary": "Comparative architectural analysis of leader-driven consensus protocols in distributed systems.",
        "content": """# Raft vs Multi-Paxos Comparative Synthesis

| Metric / Dimension | Raft Consensus | Multi-Paxos |
|---|---|---|
| **Primary Design Goal** | **Understandability** & formal decomposition | Minimal message round-trips |
| **Leader Structure** | **Strong Leader**: Log entries flow strictly from leader to followers | **Weak Leader**: Any proposer can initiate; leader is an optimization |
| **Log Gaps** | **No Gaps**: Logs are strictly contiguous sequences | **Log Gaps Allowed**: Out-of-order slots can be committed |
| **Leader Election Rule** | Candidate must hold **all committed entries** | Proposer may be missing entries and must fill gaps during Phase 1 |
| **State Machine Safety** | Enforced by log comparison in RequestVote | Enforced by Phase 1 prepare/promise quorum intersection |
| **Industrial Adoption** | etcd, Consul, TiKV, CockroachDB | Google Chubby, Spanner, Apache ZooKeeper (ZAB variant) |

### Key Architectural Trade-off
Raft's strong leader invariant eliminates the complex phase of reconciling log gaps that plagues Multi-Paxos implementations, at the minor expense of rejecting candidates that do not possess the longest log."""
    },
    {
        "slug": "b-trees-vs-lsm-trees",
        "title": "B+Trees vs Log-Structured Merge (LSM) Trees",
        "summary": "Storage engine performance trade-offs under write amplification, read latency, and disk layout.",
        "content": """# B+Trees vs LSM-Trees Storage Engine Comparison

| Feature | B+Tree (e.g. Postgres, InnoDB, SQLite) | LSM-Tree (e.g. RocksDB, Cassandra) |
|---|---|---|
| **Write Pattern** | In-place random page writes ($4\\text{KB}-16\\text{KB}$) | Append-only sequential writes (WAL + SSTables) |
| **Write Amplification (WAF)** | Very high ($10-100\\times$) due to small writes dirtying full pages | Moderate to low ($10-30\\times$) during compaction |
| **Point Read Latency** | **Fast**: Exactly 1 page access via B+Tree traversal | Requires checking MemTable + Bloom filters + multiple SSTables |
| **Range Scans** | Fast: Doubly-linked leaf pages provide sequential scanning | Requires multi-way merge sort across active SSTables |
| **Flash / SSD Wear** | High wear due to random write page rewrites | Lower wear due to sequential block allocations |
| **Optimal Workload** | Read-heavy, OLTP transactions | Write-heavy, time-series, logging, distributed stores |"""
    },
    {
        "slug": "optimistic-vs-pessimistic-concurrency",
        "title": "Optimistic (OCC) vs Pessimistic (2PL) Concurrency",
        "summary": "Trade-offs between lock-based locking and validation-based transaction processing under contention.",
        "content": """# Optimistic vs Pessimistic Concurrency Control

| Parameter | Pessimistic (Strict 2PL) | Optimistic (OCC) |
|---|---|---|
| **Locking Strategy** | Acquires locks before reading/writing data | No locks acquired during execution phase |
| **Contention Tolerance** | Performs well under **high contention**; serializes access | Suffers catastrophic abort storms under high contention |
| **Overhead under Low Contention**| High overhead: lock acquisition and bookkeeping | Minimal overhead: zero lock contention or mutex stalls |
| **Deadlock Possibility** | High: requires timeout or deadlock detection graph | Zero: transactions never wait for locks |
| **Wasted Computation** | Low: transactions wait instead of aborting | High: transactions abort after computing full results |"""
    },
    {
        "slug": "tcp-vs-udp-transport",
        "title": "TCP vs UDP Transport Layer Protocols",
        "summary": "Reliability, flow control, and latency characteristics of transport layer protocols.",
        "content": """# TCP vs UDP Comparative Analysis

| Feature | Transmission Control Protocol (TCP) | User Datagram Protocol (UDP) |
|---|---|---|
| **Connection Model** | Connection-oriented (3-Way Handshake SYN/ACK) | Connectionless datagrams |
| **Reliability Guarantee** | Guaranteed delivery, in-order sequencing, retransmissions | Best-effort delivery; packet loss and reordering allowed |
| **Flow & Congestion Control**| Sliding window flow control, Reno/Cubic/BBR congestion control | None (application must manage rate) |
| **Header Overhead** | 20–60 bytes | 8 bytes |
| **Head-of-Line Blocking** | Present: lost packet delays all subsequent bytes | Absent: independent datagram processing |
| **Primary Use Cases** | Web (HTTP/1.1, HTTP/2), SSH, Database connections | Real-time gaming, DNS, VoIP, QUIC (HTTP/3) |"""
    },
    {
        "slug": "level-triggered-vs-edge-triggered-epoll",
        "title": "Level-Triggered vs Edge-Triggered Epoll",
        "summary": "Notification semantics and event loop architectures in Linux I/O multiplexing.",
        "content": """# Level-Triggered vs Edge-Triggered Epoll

| Metric | Level-Triggered (Default) | Edge-Triggered (`EPOLLET`) |
|---|---|---|
| **Notification Trigger** | Signals as long as buffer has data available | Signals **only when buffer state transitions** (empty $\\to$ non-empty) |
| **Loop Requirement** | Can read a chunk and return to event loop | **Must loop read() until `EAGAIN` / `EWOULDBLOCK`** |
| **Risk of Starvation** | Can starve other connections if loop stays on one socket | Mitigated by bounded batching; unread data causes silent lockups |
| **Ease of Programming** | Low complexity; standard non-blocking I/O | High complexity: missing one byte can permanently stall socket |
| **System Call Overhead** | Slightly higher due to repeated notifications | Lowest system call overhead for ultra-high concurrency |"""
    }
]

EECS_TRAPS = [
    {
        "slug": "split-brain-consensus-even-quorum",
        "title": "The Split-Brain Consensus Trap: Even-Numbered Cluster Quorums",
        "domain": "Computer Science",
        "tags": ["distributed-systems", "raft", "anti-pattern", "fault-tolerance"],
        "content": """# System Design Trap: Even-Numbered Consensus Quorums

### Failure Scenario
An engineering team deploys a distributed consensus cluster (e.g. etcd, ZooKeeper, Raft) with **4 nodes** thinking it will provide higher availability than a **3-node cluster**.

### The Mathematical Trap
In a consensus system of $N$ nodes, the majority quorum required to commit transactions is:
$$Q = \\left\\lfloor \\frac{N}{2} \\right\\rfloor + 1$$

- For $N = 3$: Quorum is $\\lfloor 3/2 \\rfloor + 1 = 2$. Tolerates $3 - 2 = 1$ failure.
- For $N = 4$: Quorum is $\\lfloor 4/2 \\rfloor + 1 = 3$. Tolerates $4 - 3 = 1$ failure!

### Why 4 Nodes is Strictly Worse than 3 Nodes
1. **Zero Additional Fault Tolerance**: Both tolerate exactly 1 node failure.
2. **Network Partition Vulnerability**: If a network partition splits the 4-node cluster into two partitions of 2 and 2, **neither partition has a majority ($2 < 3$)**, rendering the entire cluster completely unavailable!
3. **Higher Failure Probability**: Four independent hardware nodes have a statistically higher chance of hardware failure than three nodes.

### Golden Rule
Consensus clusters should **always use an odd number of voting nodes** ($2F + 1$ nodes to tolerate $F$ failures)."""
    },
    {
        "slug": "false-sharing-in-multicore-cache-lines",
        "title": "False Sharing in Multi-Core CPU Caches",
        "domain": "Computer Science",
        "tags": ["concurrency", "multithreading", "hardware", "anti-pattern"],
        "content": """# Concurrency Trap: False Sharing

### The Anti-Pattern
Two threads executing on separate CPU cores modify independent variables that happen to share the same **64-byte hardware cache line**.

```c
struct Counter {
    uint64_t thread1_count; // Core 0 modifies this
    uint64_t thread2_count; // Core 1 modifies this
}; // Both variables sit inside the same 64-byte L1 cache line!
```

### Underlying Mechanism
Hardware cache coherence (MESI) operates on **cache line granularity (64 bytes)**, not individual word/variable granularity.
1. Core 0 writes to `thread1_count` $\\to$ transitions cache line to Modified (M) $\\to$ invalidates Core 1's cache line (I).
2. Core 1 attempts to write to `thread2_count` $\\to$ suffers a cache miss $\\to$ issues RWITM $\\to$ invalidates Core 0's cache line.
3. The cache line ping-pongs over the inter-core interconnect, degrading multi-threaded throughput by $10\\times-50\\times$!

### Remediation
Pad independent variables to 64-byte boundaries using `alignas(64)` or `__attribute__((aligned(64)))`."""
    },
    {
        "slug": "aba-problem-in-lockfree-concurrency",
        "title": "The ABA Problem in Lock-Free Compare-And-Swap (CAS)",
        "domain": "Computer Science",
        "tags": ["concurrency", "lock-free", "cas", "memory-management"],
        "content": """# Lock-Free Concurrency Trap: The ABA Problem

### The Bug Mechanism
In lock-free algorithms using atomic Compare-And-Swap (`CAS(&ptr, old_val, new_val)`):
1. Thread 1 reads pointer $A$ pointing to node $A$.
2. Thread 1 is preempted.
3. Thread 2 pops node $A$, frees it, pops node $B$, and re-allocates memory for a new node which happens to be allocated at memory address $A$!
4. Thread 1 resumes and executes `CAS(&ptr, A, B)`.
5. The CAS succeeds because the raw pointer address is still $A$, but the internal node contents and linked pointers are completely corrupted!

### Remediation
- Use **tagged pointers** / generational version counters (e.g. 64-bit address + 64-bit monotonically increasing counter with double-width `cmpxchg16b`).
- Use **Hazard Pointers** or Epoch-Based Reclamation (EBR) to prevent memory reuse while active references exist."""
    },
    {
        "slug": "epoll-starvation-edge-triggered",
        "title": "Socket Starvation in Edge-Triggered Epoll Loops",
        "domain": "Computer Science",
        "tags": ["linux", "epoll", "networking", "anti-pattern"],
        "content": """# Network Systems Trap: Socket Starvation in Edge-Triggered Epoll

### The Trap
When using edge-triggered epoll (`EPOLLET`), an event loop reads from a socket in an unbounded loop until `EAGAIN`:
```c
while ((n = read(fd, buf, sizeof(buf))) > 0) {
    process(buf, n);
}
```
If a high-bandwidth client continuously streams data faster than the application can process it, this single socket **starves all other ready connections** registered on the epoll instance!

### Remediation
Process data in bounded batches (e.g., maximum 64KB or 5 reads per event loop turn). If data remains, requeue the file descriptor to the end of the application's user-space work queue."""
    },
    {
        "slug": "dirty-reads-under-read-committed-isolation",
        "title": "Non-Repeatable Reads & Phantom Records in Database Isolation",
        "domain": "Computer Science",
        "tags": ["databases", "transactions", "acid", "anti-pattern"],
        "content": """# Database Isolation Trap: Read-Committed vs Serializable

### The Misconception
Developers frequently assume that standard database transactions prevent concurrent anomalies. In PostgreSQL and MySQL, the default isolation level is **Read Committed** (or Repeatable Read).

### Anomalies Permitted Under Weak Isolation
1. **Non-Repeatable Read**: Reading the same row twice within a single transaction yields different values because a concurrent transaction committed a modification in between.
2. **Phantom Read**: Re-running a `SELECT WHERE` query returns newly inserted rows committed by another transaction.
3. **Write Skew**: Two concurrent transactions read overlapping state, make independent modifications that satisfy local constraints, but violate the combined global invariant.

### Remediation
Use `SERIALIZABLE` isolation with retry logic for write-skew sensitive operations, or use `SELECT ... FOR UPDATE` row locks."""
    }
]

EECS_FLASHCARDS = [
    {
        "type": "cloze",
        "text": "In the Raft consensus protocol, an election timeout triggers a follower to transition to the {{c1::Candidate}} state, increment its {{c2::currentTerm}}, and broadcast {{c3::RequestVote RPCs}} to all peers.",
        "pearl": "Randomized timeouts (150ms-300ms) prevent split-vote livelocks in Raft leader election.",
        "tags": ["MIT_6.033", "Distributed-Systems", "Consensus", "Raft"],
        "source": "concepts/raft-distributed-consensus.md",
        "wiki_slug": "concepts/raft-distributed-consensus.md",
        "course": "MIT 6.033",
        "domain": "Computer Science",
        "system": "Distributed Systems",
        "difficulty": 2
    },
    {
        "type": "cloze",
        "text": "A distributed consensus cluster of $2F + 1$ nodes requires a majority quorum of {{c1::F + 1}} nodes to commit a log entry, allowing it to tolerate up to {{c2::F}} concurrent node crash failures.",
        "pearl": "Even-numbered clusters provide zero extra fault tolerance and increase split-brain risk.",
        "tags": ["MIT_6.033", "Distributed-Systems", "Consensus", "Quorum"],
        "source": "exam_traps/split-brain-consensus-even-quorum.md",
        "wiki_slug": "exam_traps/split-brain-consensus-even-quorum.md",
        "course": "MIT 6.033",
        "domain": "Computer Science",
        "system": "Distributed Systems",
        "difficulty": 2
    },
    {
        "type": "differential",
        "text": "Compared to B+Trees which perform in-place random page updates, Log-Structured Merge (LSM) Trees convert random writes into sequential disk writes using an in-memory {{c1::MemTable}} and background {{c2::compaction}}.",
        "pearl": "LSM-Trees optimize write throughput at the cost of higher read amplification and compaction overhead.",
        "tags": ["MIT_6.033", "Storage", "Databases", "LSM-Tree"],
        "source": "differentials/b-trees-vs-lsm-trees.md",
        "wiki_slug": "differentials/b-trees-vs-lsm-trees.md",
        "course": "MIT 6.033",
        "domain": "Computer Science",
        "system": "Storage Engines",
        "difficulty": 2
    },
    {
        "type": "cloze",
        "text": "Under the MESI cache coherence protocol, a cache line in the {{c1::Shared (S)}} state must broadcast an {{c2::Invalidation}} signal over the bus before a processor core can perform a write operation.",
        "pearl": "Invalidation broadcasts transition the local cache line from Shared to Modified (M).",
        "tags": ["MIT_6.004", "Architecture", "Hardware", "Cache-Coherence"],
        "source": "concepts/cache-coherence-mesi-protocol.md",
        "wiki_slug": "concepts/cache-coherence-mesi-protocol.md",
        "course": "MIT 6.004",
        "domain": "Computer Science",
        "system": "Computer Architecture",
        "difficulty": 2
    },
    {
        "type": "cloze",
        "text": "The Write-Ahead Logging (WAL) invariant dictates that log records describing a database update must be flushed to non-volatile disk {{c1::before}} the corresponding dirty data page is written to disk.",
        "pearl": "WAL guarantees atomicity and durability by enabling REDO and UNDO crash recovery passes.",
        "tags": ["MIT_6.033", "Databases", "Durability", "WAL"],
        "source": "concepts/write-ahead-logging-and-recovery.md",
        "wiki_slug": "concepts/write-ahead-logging-and-recovery.md",
        "course": "MIT 6.033",
        "domain": "Computer Science",
        "system": "Database Systems",
        "difficulty": 1
    },
    {
        "type": "cloze",
        "text": "Linux epoll scales to tens of thousands of concurrent connections because it monitors file descriptors using an in-kernel {{c1::Red-Black Tree}} for registered descriptors and a {{c2::Doubly-Linked List}} for active ready events.",
        "pearl": "Replaces the O(N) linear scanning overhead of select() and poll() with O(1) ready list retrieval.",
        "tags": ["MIT_6.033", "Linux", "Networking", "Epoll"],
        "source": "concepts/epoll-scalable-io-multiplexing.md",
        "wiki_slug": "concepts/epoll-scalable-io-multiplexing.md",
        "course": "MIT 6.033",
        "domain": "Computer Science",
        "system": "Systems Programming",
        "difficulty": 2
    },
    {
        "type": "trap",
        "text": "In edge-triggered epoll (`EPOLLET`), the application must execute non-blocking reads in a loop until receiving an {{c1::EAGAIN or EWOULDBLOCK}} error, or risk permanently missing subsequent unread data.",
        "pearl": "Edge-triggered mode notifies the application only when state transitions occur.",
        "tags": ["MIT_6.033", "Linux", "Networking", "Anti-Pattern"],
        "source": "exam_traps/epoll-starvation-edge-triggered.md",
        "wiki_slug": "exam_traps/epoll-starvation-edge-triggered.md",
        "course": "MIT 6.033",
        "domain": "Computer Science",
        "system": "Systems Programming",
        "difficulty": 2
    },
    {
        "type": "cloze",
        "text": "In 64-bit x86 virtual memory with 4-level paging, a TLB miss requires {{c1::4}} sequential main memory accesses to traverse PML4, PDPT, PD, and PT before resolving the physical address.",
        "pearl": "A high TLB hit rate (>99%) is critical for pipeline performance.",
        "tags": ["MIT_6.004", "Architecture", "Virtual-Memory", "TLB"],
        "source": "concepts/virtual-memory-and-tlb.md",
        "wiki_slug": "concepts/virtual-memory-and-tlb.md",
        "course": "MIT 6.004",
        "domain": "Computer Science",
        "system": "Computer Architecture",
        "difficulty": 2
    },
    {
        "type": "differential",
        "text": "According to the CAP theorem, during a network partition ($P$), a distributed data store must choose between returning an error or blocking to ensure {{c1::Consistency ($C$)}}, or returning potentially stale data to guarantee {{c2::Availability ($A$)}}.",
        "pearl": "The PACELC theorem extends CAP: if partitioned, choose A or C; else, choose Latency (L) or Consistency (C).",
        "tags": ["MIT_6.033", "Distributed-Systems", "Theory", "CAP-Theorem"],
        "source": "concepts/cap-theorem-and-pacelc.md",
        "wiki_slug": "concepts/cap-theorem-and-pacelc.md",
        "course": "MIT 6.033",
        "domain": "Computer Science",
        "system": "Distributed Systems",
        "difficulty": 1
    },
    {
        "type": "trap",
        "text": "False sharing in multi-threaded programs occurs when two CPU cores independently modify separate variables located within the same {{c1::64-byte cache line}}, causing high-latency bus invalidation ping-pong.",
        "pearl": "Remediated by aligning independent variables to 64-byte boundaries with alignas(64).",
        "tags": ["MIT_6.004", "Concurrency", "Hardware", "Anti-Pattern"],
        "source": "exam_traps/false-sharing-in-multicore-cache-lines.md",
        "wiki_slug": "exam_traps/false-sharing-in-multicore-cache-lines.md",
        "course": "MIT 6.004",
        "domain": "Computer Science",
        "system": "Computer Architecture",
        "difficulty": 3
    }
]
