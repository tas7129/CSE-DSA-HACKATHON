package edu.demo.exam.model;

import java.util.*;

/** Undirected conflict graph; public course identifiers are one-based. */
public final class ConflictGraph {
    private final List<Set<Integer>> neighbours;
    public ConflictGraph(int courses) {
        if (courses < 1) throw new IllegalArgumentException("Number of courses must be positive.");
        neighbours = new ArrayList<>(courses);
        for (int i=0;i<courses;i++) neighbours.add(new LinkedHashSet<>());
    }
    public int size(){ return neighbours.size(); }
    public int edgeCount(){ return neighbours.stream().mapToInt(Set::size).sum()/2; }
    public Set<Integer> neighbours(int course){ check(course); return Collections.unmodifiableSet(neighbours.get(course-1)); }
    public int degree(int course){ return neighbours(course).size(); }
    public boolean adjacent(int a,int b){ check(a);check(b);return neighbours.get(a-1).contains(b-1); }
    public void addConflict(int a,int b){ check(a);check(b);if(a==b)throw new IllegalArgumentException("A course cannot conflict with itself."); neighbours.get(a-1).add(b-1);neighbours.get(b-1).add(a-1); }
    private void check(int c){if(c<1||c>size())throw new IllegalArgumentException("Course identifier must be between 1 and "+size()+".");}
}
