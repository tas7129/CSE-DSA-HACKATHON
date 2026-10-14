package edu.demo.exam.algorithm;

import edu.demo.exam.model.*;import edu.demo.exam.util.TimetableValidator;import java.util.*;

/** Exact capacitated coloring with DSatur vertex selection, symmetry breaking and a time limit. */
public final class ExactSolver {
    public Timetable solve(ConflictGraph g,int capacity,long timeLimitMillis,Timetable initial){if(capacity<1||timeLimitMillis<1)throw new IllegalArgumentException("Capacity and time limit must be positive.");if(initial==null)initial=new DSaturSolver().solve(g,capacity);TimetableValidator.requireValid(g,capacity,initial);long start=System.nanoTime(),deadline=start+timeLimitMillis*1_000_000L;Search s=new Search(g,capacity,deadline,initial.assignments(),initial.slotCount(),initial.assignmentOrder());s.run(0,0);Timetable result=new Timetable(s.best,System.nanoTime()-start,!s.timedOut,s.timedOut,s.bestOrder);TimetableValidator.requireValid(g,capacity,result);return result;}
    private static final class Search {final ConflictGraph g;final int cap,n;final long deadline;int[] color,best;int[] sizes;int bestCount;boolean timedOut;List<Integer> bestOrder,path=new ArrayList<>();Search(ConflictGraph g,int cap,long d,int[] initial,int k,List<Integer> initialOrder){this.g=g;this.cap=cap;n=g.size();deadline=d;best=initial.clone();bestCount=k;bestOrder=new ArrayList<>(initialOrder);sizes=new int[n];color=new int[n];Arrays.fill(color,-1);}
        void run(int assigned,int used){if(System.nanoTime()>=deadline){timedOut=true;return;}if(assigned==n){if(used<bestCount){bestCount=used;best=color.clone();bestOrder=List.copyOf(path);}return;}if(used>=bestCount||Math.max(used,(n+cap-1)/cap)>=bestCount)return;
            int v=select();boolean[] blocked=new boolean[used];for(int u:g.neighbours(v+1))if(color[u]>=0)blocked[color[u]]=true;
            for(int c=0;c<=used&&c<bestCount;c++){if(c<used&&(blocked[c]||sizes[c]>=cap))continue;if(c==used&&used+1>=bestCount)continue;color[v]=c;sizes[c]++;path.add(v+1);run(assigned+1,Math.max(used,c+1));path.remove(path.size()-1);sizes[c]--;color[v]=-1;if(timedOut)return;}
        }
        int select(){int v=-1,bs=-1,bd=-1;for(int x=0;x<n;x++)if(color[x]<0){Set<Integer> sat=new HashSet<>();for(int u:g.neighbours(x+1))if(color[u]>=0)sat.add(color[u]);int d=g.degree(x+1);if(sat.size()>bs||(sat.size()==bs&&(d>bd||(d==bd&&x<v)))){v=x;bs=sat.size();bd=d;}}return v;}
    }
}
