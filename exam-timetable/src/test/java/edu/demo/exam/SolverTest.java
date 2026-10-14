package edu.demo.exam;

import edu.demo.exam.algorithm.*;import edu.demo.exam.model.*;import edu.demo.exam.util.*;import org.junit.jupiter.api.Test;import static org.junit.jupiter.api.Assertions.*;

class SolverTest {
 @Test void isolatedCoursesFitCapacityAndAreValidated(){ConflictGraph g=new ConflictGraph(5);Timetable t=new DSaturSolver().solve(g,3);assertEquals(2,t.slotCount());assertNull(TimetableValidator.validate(g,3,t));}
 @Test void completeGraphRequiresOneSlotPerCourse(){ConflictGraph g=new ConflictGraph(5);for(int i=1;i<=5;i++)for(int j=i+1;j<=5;j++)g.addConflict(i,j);Timetable t=new ExactSolver().solve(g,3,5000,new DSaturSolver().solve(g,3));assertTrue(t.optimal());assertEquals(5,t.slotCount());}
 @Test void capacityCanForceAdditionalSlots(){ConflictGraph g=new ConflictGraph(4);Timetable t=new ExactSolver().solve(g,1,3000,new DSaturSolver().solve(g,1));assertEquals(4,t.slotCount());assertTrue(t.optimal());}
 @Test void duplicateEdgesAreSafeAndRandomSeedIsReproducible(){ConflictGraph g=new ConflictGraph(3);g.addConflict(1,2);g.addConflict(1,2);assertEquals(1,g.edgeCount());assertEquals(GraphGenerator.random(20,.4,99).edgeCount(),GraphGenerator.random(20,.4,99).edgeCount());}
 @Test void invalidInputsAreRejected(){ConflictGraph g=new ConflictGraph(3);assertThrows(IllegalArgumentException.class,()->g.addConflict(1,4));assertThrows(IllegalArgumentException.class,()->g.addConflict(2,2));assertThrows(IllegalArgumentException.class,()->new DSaturSolver().solve(g,0));}
 @Test void exactSolverFindsValidColoringForOddCycle(){ConflictGraph g=new ConflictGraph(5);for(int i=1;i<=5;i++)g.addConflict(i,i%5+1);Timetable seed=new DSaturSolver().solve(g,5);Timetable t=new ExactSolver().solve(g,5,3000,seed);assertTrue(t.optimal());assertEquals(3,t.slotCount());assertNull(TimetableValidator.validate(g,5,t));}
}
