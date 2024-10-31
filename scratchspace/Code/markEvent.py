import globals as glb
# import matlab

def markEvent(EventType: str, PARAMETERS=None, *args, **kwargs):
    """
    Log events during the experiment with standardized event names and timing.
    
    Parameters:
    ----------
    EventType : str
        The type of event to log (e.g., 'taskStart', 'trialStart').
    PARAMETERS : Parameters, optional
        The Parameters instance where events will be stored.
    *args : tuple
        Positional arguments for event specifics.
    **kwargs : dict
        Additional keyword arguments like 'trialIdx' or 'blockIdx'.
    """
    # Get the event time using the global clock
    eventTime = glb.ABS_CLOCK.getTime()
    
    # Define event names based on EventType and additional arguments
    eventName = ""
    match EventType:
        case "taskStart":
            eventName = "Task Started"
        case "taskStop":
            eventName = "Task Ended Successfully"
        case "taskAbort":
            eventName = "Task Aborted"
        case "introStart":
            eventName = "Intro Started"
        case "introEnd":
            eventName = "Intro Ended"
        case "blockStart":
            eventName = f"Block {kwargs.get('blockIdx', '')} Started"
        case "blockEnd":
            eventName = f"Block {kwargs.get('blockIdx', '')} Ended"
        case "trialStart":
            eventName = f"Trial {kwargs.get('trialIdx', '')} in Block {kwargs.get('blockIdx', '')} Started"
        case "trialEnd":
            eventName = f"Trial {kwargs.get('trialIdx', '')} in Block {kwargs.get('blockIdx', '')} Ended"
        case "DecisionStart":
            eventName = "Decision Phase Started"
        case "DecisionEnd":
            eventName = "Decision Phase Ended"
        case "UserChoice":
            eventName = f"User Made Choice {kwargs.get('choice', '')}"
        case "OutcomeStart":
            eventName = "Outcome Phase Started"
        case "OutcomeEnd":
            eventName = "Outcome Phase Ended"
        case "TrustworthyRankStart":
            eventName = f"Trustworthy Ranking Started {kwargs.get('rank', '')}"
        case "TrustworthyRankEnd":
            eventName = f"Trustworthy Ranking Ended {kwargs.get('rank', '')}"
        case _:
            eventName = "UNKNOWN EVENT"

    # Append the event and time to PARAMETERS' events list, if provided
    # if PARAMETERS:
    #     PARAMETERS.events.append((eventName, eventTime))
    glb.EVENTS.append((eventName, eventTime))

    # Additional environment-specific handling if needed
    # if PARAMETERS and PARAMETERS.ID.get('expEnv') == "BCM-EMU":
    #     match EventType:
    #         case "taskStart":
    #             onlineNSP = glb.MATENG.eval("TaskComment('start', emuSaveName);", nargout=1)
    #             glb.MATENG.workspace['onlineNSP'] = matlab.double(onlineNSP)
    #         case "taskStop":
    #             glb.MATENG.eval("TaskComment('stop', emuSaveName);", nargout=0)
    #         case "taskAbort":
    #             glb.MATENG.eval("TaskComment('kill', emuSaveName);", nargout=0)
    #         case _:
    #             blackRockComment = glb.MATENG.cellstr([eventName])
    #             glb.MATENG.workspace['blackRockComment'] = blackRockComment
    #             glb.MATENG.eval("blackRockComment = [blackRockComment{:}];", nargout=0)
    #             glb.MATENG.eval("for i=1:numel(onlineNSP); cbmex('comment', 255, 0, blackRockComment, 'instance', onlineNSP(i)-1); end", nargout=0)
