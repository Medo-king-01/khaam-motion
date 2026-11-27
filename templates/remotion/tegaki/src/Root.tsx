import { Composition } from 'remotion';
import { ArabicHandwriting } from './ArabicHandwriting';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="ArabicHandwriting"
    component={ArabicHandwriting}
    durationInFrames={180}
    fps={30}
    width={1080}
    height={1920}
  />
);
