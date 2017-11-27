import unittest
import build_program
import build_expressions
import build_primitives
import build_structures
import build_program
import build_lines



class TestSend(unittest.TestCase):
    def test_make_send(self):
        pr = build_program.ProgramRouter(debug=False)
        ar = pr.makeAgentRouter('agent1')
        sr = ar.makeSubagentRouter('subagent1')

        agentScope = build_program.AgentScope()
        subagentScope = build_program.SubagentScope(agentScope)

        line = build_program.Node(6,'a -> b')
        result = build_lines.buildLine(line,subagentScope,sr)
        # TODO: Actually test something here


    def test_make_assign(self):
        pr = build_program.ProgramRouter(debug=False)
        ar = pr.makeAgentRouter('agent1')
        sr = ar.makeSubagentRouter('subagent1')

        agentScope = build_program.AgentScope()
        subagentScope = build_program.SubagentScope(agentScope)

        line = build_program.Node(6,'n = 3')
        result = build_lines.buildLine(line,subagentScope,sr)
        self.assertEqual(subagentScope.getLocals(),{})
        result.exe()
        self.assertEqual(subagentScope.getLocals(),{'n':3})

