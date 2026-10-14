package edu.demo.exam.util;
import edu.demo.exam.model.ConflictGraph;import java.util.Random;
public final class GraphGenerator {private GraphGenerator(){} public static ConflictGraph random(int n,double density,long seed){if(n<1)throw new IllegalArgumentException("Number of courses must be positive.");if(density<0||density>1||!Double.isFinite(density))throw new IllegalArgumentException("Density must be between 0 and 1.");ConflictGraph g=new ConflictGraph(n);Random r=new Random(seed);for(int i=1;i<=n;i++)for(int j=i+1;j<=n;j++)if(r.nextDouble()<density)g.addConflict(i,j);return g;}}
