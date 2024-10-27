import Code.globals as glb
import matlab

def markEvent(EventType:str, *args):
    eventName=''
    eventTime=glb.ABS_CLOCK.getTime()
    match EventType:
        case "taskStart":
            eventName = "Task Started"
        case "taskStop":
            eventName = "Task Ended Successfully"
        case "taskAbort":
            eventName = "Task Aborted"

        case "introStart":
            eventName = f"Intro Started"
        case "introEnd":
            eventName = f"Intro Ended"

        case "blockStart":
            eventName = f"Block {args[0]} Started"
        case "blockEnd":
            eventName = f"Block {args[0]} Ended"
        case "trialStart":
            eventName = f"Trial {args[0]} Started"
        case "trialEnd":
            eventName = f"Trial {args[0]} Ended"
        case "trialBlockStart":
            eventName = f"Trial {args[0]} in Block {args[1]} Started"
        case "trialBlockEnd":
            eventName = f"Trial {args[0]} in Block {args[1]} Ended"

        case "DecisionStart":
            eventName = f"Decison Phase {args[0]} Started"
        case "DecisionEnd":
            eventName=f"Decision Phase {args[0]} Ended"
        case "UserChoice":
            eventName=f"User Made Choice {args[0]}"
        case "OtherChoice":
            eventName=f"Other Made Choice {args[0]}"
        case "OutcomeStart":
            eventName= f"Outcome Phase {args[0]} Started"
        case "OutcomeEnd":
            eventName= f"Outcome Phase {args[0]} Ended"
        case "LotteryStart":
            eventName=f"Lottery Phase {args[0]} Started"
        case "LotteryEnded":
            eventName=f"Lottery Phase {args[0]} Started"
        case "AdviceGiven":
            eventName=f"Advice was Given {args[0]}"
        case "AdviceEnded":
            eventName=f"Advice was Ended {args[0]}"
        case "LotteryChoice":
            eventName=f"User made Choice {args[0]}"
        case "TrustworthyRankStart":
            eventName=f"Trustworthy ranking made {args[0]}"
        case "TrustworthyRankEnd":
            eventName=f"Trustworthy rankind ended {args[0]}"

        case _:
            eventName = f'UNKNOWN EVENT'    
    glb.PARAMETERS.events.append((eventName, eventTime))

        
    match glb.PARAMETERS.ID['expEnv']:
        case "BCM-EMU":
            match EventType:
                case "taskStart":
                    onlineNSP = glb.MATENG.eval("TaskComment('start', emuSaveName);", nargout = 1)
                    glb.MATENG.workspace['onlineNSP'] = matlab.double(onlineNSP)
                case "taskStop":
                    glb.MATENG.eval("TaskComment('stop', emuSaveName);", nargout = 0)
                case "taskAbort":
                    glb.MATENG.eval("TaskComment('kill', emuSaveName);", nargout = 0)
                case _:
                    blackRockComment = glb.MATENG.cellstr(list(eventName))
                    glb.MATENG.workspace['blackRockComment'] = blackRockComment
                    glb.MATENG.eval("blackRockComment = [blackRockComment{:}];", nargout = 0)
                    glb.MATENG.eval("for i=1:numel(onlineNSP); cbmex('comment', 255, 0, blackRockComment,'instance',onlineNSP(i)-1); end", nargout = 0)   