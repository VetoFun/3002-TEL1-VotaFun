import { useRef } from 'react';

interface SelectProps {
  label: string;
  options: string[];
  onChange?: (event: React.ChangeEvent<HTMLSelectElement>) => void;
}

const Select = ({ label, options, onChange }: SelectProps) => {
  const selectRef = useRef<HTMLSelectElement>(null);

  return (
    <select className="select select-bordered select-error w-full text-xl" ref={selectRef} onChange={onChange}>
      <option disabled selected>
        {label}
      </option>
      {options.map((option, index) => (
        <option value={option} key={index}>
          {option}
        </option>
      ))}
    </select>
  );
};

export { Select };
