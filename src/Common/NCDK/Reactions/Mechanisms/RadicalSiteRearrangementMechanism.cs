/* Copyright (C) 2008  Miguel Rojas <miguelrojasch@yahoo.es>
 *
 * Contact: cdk-devel@lists.sourceforge.net
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation; either version 2.1
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT Any WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 */

using NCDK.Tools.Manipulator;
using System;
using System.Collections.Generic;
using System.Linq;

namespace NCDK.Reactions.Mechanisms
{
    /// <summary>
    /// <para>This mechanism displaces an Atom or substructure (R) from one position to an other.
    /// It returns the reaction mechanism which has been cloned the <see cref="IAtomContainer"/>.</para>
    /// <para>This reaction could be represented as [A*]-(X)_n-Y-Z =&gt; A(Z)-(X)_n-[Y*]</para>
    /// </summary>
    // @author         miguelrojasch
    // @cdk.created    2008-02-10
    // @cdk.module     reaction
    public class RadicalSiteRearrangementMechanism : IReactionMechanism
    {
        /// <summary>
        /// Initiates the process for the given mechanism. The atoms to apply are mapped between
        /// reactants and products.
        /// </summary>
        /// <param name="atomContainerSet"></param>
        /// <param name="atomList">
        /// The list of atoms taking part in the mechanism. Only allowed two atoms.
        ///                    The first atom is the atom which must be moved and the second
        ///                    is the atom which receives the atom1 and the third is the atom which loss
        ///                    the first atom</param>
        /// <param name="bondList">The list of bonds taking part in the mechanism. Only allowed one bond.
        ///                       It is the bond which is moved</param>
        /// <returns>The Reaction mechanism</returns>
        public IReaction Initiate(IChemObjectSet<IAtomContainer> atomContainerSet, IList<IAtom> atomList, IList<IBond> bondList)
        {
            var atMatcher = CDK.AtomTypeMatcher;
            if (atomContainerSet.Count != 1)
            {
                throw new CDKException("RadicalSiteRearrangementMechanism only expects one IAtomContainer");
            }
            if (atomList.Count != 3)
            {
                throw new CDKException("RadicalSiteRearrangementMechanism expects three atoms in the List");
            }
            if (bondList.Count != 1)
            {
                throw new CDKException("RadicalSiteRearrangementMechanism only expect one bond in the List");
            }
            IAtomContainer molecule = atomContainerSet[0];
            IAtomContainer reactantCloned;
            reactantCloned = (IAtomContainer)molecule.Clone();
            IAtom atom1 = atomList[0];// Atom to be moved
            IAtom atom1C = reactantCloned.Atoms[molecule.Atoms.IndexOf(atom1)];
            IAtom atom2 = atomList[1];// Atom to receive the new bonding with a ISingleElectron
            IAtom atom2C = reactantCloned.Atoms[molecule.Atoms.IndexOf(atom2)];
            IAtom atom3 = atomList[2];// Atom which loss the atom
            IAtom atom3C = reactantCloned.Atoms[molecule.Atoms.IndexOf(atom3)];
            IBond bond1 = bondList[0];// Bond to move
            int posBond1 = molecule.Bonds.IndexOf(bond1);

            reactantCloned.Bonds.Remove(reactantCloned.Bonds[posBond1]);
            IBond newBond = atom1.Builder.NewBond(atom1C, atom2C, BondOrder.Single);
            reactantCloned.Bonds.Add(newBond);

            var selectron = reactantCloned.GetConnectedSingleElectrons(atom2C);
            reactantCloned.SingleElectrons.Remove(selectron.Last());
            atom2C.Hybridization = Hybridization.Unset;
            AtomContainerManipulator.PercieveAtomTypesAndConfigureAtoms(reactantCloned);
            IAtomType type = atMatcher.FindMatchingAtomType(reactantCloned, atom2C);
            if (type == null || type.AtomTypeName.Equals("X", StringComparison.Ordinal))
                return null;

            reactantCloned.SingleElectrons.Add(atom2C.Builder.NewSingleElectron(atom3C));
            atom3C.Hybridization = Hybridization.Unset;
            AtomContainerManipulator.PercieveAtomTypesAndConfigureAtoms(reactantCloned);
            type = atMatcher.FindMatchingAtomType(reactantCloned, atom3C);
            if (type == null || type.AtomTypeName.Equals("X", StringComparison.Ordinal))
                return null;

            IReaction reaction = atom2C.Builder.NewReaction();
            reaction.Reactants.Add(molecule);

            /* mapping */
            foreach (var atom in molecule.Atoms)
            {
                IMapping mapping = atom2C.Builder.NewMapping(atom,
                        reactantCloned.Atoms[molecule.Atoms.IndexOf(atom)]);
                reaction.Mappings.Add(mapping);
            }

            reaction.Products.Add(reactantCloned);

            return reaction;
        }
    }
}
